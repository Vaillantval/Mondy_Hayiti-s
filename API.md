# MatStore Haiti — API REST

**Base URL** : `https://matstorehaiti.online/api/`
**Auth** : Bearer JWT (`Authorization: Bearer <access_token>`)
**Docs interactives** : `/api/docs/` (Swagger) · `/api/redoc/` (ReDoc)
**Format des erreurs** :
```json
{ "success": false, "error": { "code": "OUT_OF_STOCK", "message": "..." } }
```

---

## Auth — `/api/auth/`

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| POST | `/auth/register/` | Public | Inscription + retourne tokens JWT |
| POST | `/auth/login/` | Public | Connexion + retourne tokens JWT |
| POST | `/auth/logout/` | Requis | Blackliste le refresh token |
| POST | `/auth/token/refresh/` | Public | Renouveler l'access token |
| GET | `/auth/me/` | Requis | Profil de l'utilisateur connecté |
| PATCH | `/auth/me/` | Requis | Modifier son profil |
| POST | `/auth/change-password/` | Requis | Changer son mot de passe |
| POST | `/auth/fcm-token/` | Requis | Enregistrer/mettre à jour le FCM token Android |

---

## Produits — `/api/products/`

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/products/` | Public | Liste paginée avec filtres |
| GET | `/products/search/?q=shea` | Public | Recherche full-text dédiée |
| GET | `/products/{slug}/` | Public | Détail d'un produit |
| GET | `/products/featured/` | Public | Produits mis en avant |
| GET | `/products/new-arrivals/` | Public | Nouveautés (30 derniers jours) |
| GET | `/products/on-sale/` | Public | Produits en promotion |

**Filtres disponibles sur `/products/` :**
```
?category=cosmetiques
?min_price=500&max_price=2000
?in_stock=true
?search=shea
?ordering=solde_price | -solde_price | created_at
```

**Recherche full-text `/products/search/` :**
```
?q=shea butter       → cherche dans nom, description, marque, catégories
```

---

## Catégories — `/api/categories/`

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/categories/` | Public | Toutes les catégories |
| GET | `/categories/{slug}/` | Public | Détail + produits de la catégorie |

---

## Accueil — `/api/sliders/`

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/sliders/` | Public | Hero slides du carrousel d'accueil |

```json
{
  "success": true,
  "count": 2,
  "results": [
    {
      "id": 1,
      "title": "Vos pâtisseries livrées en Haïti",
      "description": "Commandez en quelques clics",
      "button_text": "Voir la boutique",
      "button_link": "/shop/",
      "image": "https://hayitis.com/media/sliders/2026/06/13/hero.jpg"
    }
  ]
}
```

`image` est une URL absolue. Les slides sont triés par date de création.

---

## Panier — `/api/cart/`

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/cart/` | Requis | Voir son panier |
| POST | `/cart/add/` | Requis | Ajouter un produit |
| PATCH | `/cart/update/{item_id}/` | Requis | Modifier la quantité |
| DELETE | `/cart/remove/{item_id}/` | Requis | Supprimer un article |
| DELETE | `/cart/clear/` | Requis | Vider le panier |

---

## Commandes — `/api/orders/`

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/orders/` | Requis | Historique des commandes |
| POST | `/orders/` | Requis | Passer une commande |
| GET | `/orders/{id}/` | Requis | Détail d'une commande |
| POST | `/orders/{id}/cancel/` | Requis | Annuler (si statut pending) |
| GET | `/orders/{id}/track/?email=x` | **Public** | Suivi commande sans authentification |

**Suivi public** — retourne uniquement : statut, is_paid, transporteur, adresse livraison, total.
Nécessite l'email du client comme vérification : `?email=client@email.com`

**Payload création commande :**
```json
{
  "items": [
    { "product_id": 1, "quantity": 2 }
  ],
  "payment_method": "moncash",
  "delivery_address": {
    "street": "Rue Lamarre",
    "city": "Pétion-Ville",
    "department": "Ouest"
  },
  "notes": "Livrer après 14h"
}
```

**`payment_method` acceptés :** `moncash` · `natcash` · `stripe` · `offline`

**Statuts commande (`status`) :** `pending` · `processing` · `shipped` · `delivered` · `canceled`

**Statuts paiement (`payment_status`) :** `unpaid` · `proof_submitted` · `verified` · `paid`

**Champs paiement hors ligne dans la réponse :**
- `payment_status` — état du paiement (`unpaid` par défaut, `proof_submitted` après upload de la preuve)
- `payment_proof_url` — URL absolue de l'image de preuve, `null` si non soumise

---

## Paiements — `/api/payments/`

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| POST | `/payments/initiate/` | Requis | Initier un paiement MonCash / NatCash / Stripe |
| POST | `/payments/verify/` | Requis | Vérifier le statut d'un paiement |
| POST | `/payments/offline/` | Requis | Soumettre une preuve de paiement hors ligne (multipart) |
| POST | `/payments/webhook/moncash/` | Public | Webhook MonCash |
| POST | `/payments/webhook/stripe/` | Public | Webhook Stripe |

**Méthodes supportées via API :** `moncash` · `natcash` · `stripe` · `offline`

---

### Paiement Hors Ligne — flux complet

Le paiement hors ligne (virement bancaire, dépôt) suit un flux en **2 étapes** :

**Étape 1 — Créer la commande avec `payment_method = "offline"` :**
```
POST /api/orders/
Content-Type: application/json

{
  "items": [{ "product_id": 1, "quantity": 2 }],
  "payment_method": "offline",
  "delivery_address": { "street": "Rue Lamarre", "city": "Pétion-Ville" }
}

→ { "success": true, "data": { "id": 42, "payment_status": "unpaid", ... } }
```

**Étape 2 — Uploader la preuve après virement / dépôt :**
```
POST /api/payments/offline/
Content-Type: multipart/form-data

order_id: 42
payment_proof: <fichier JPG ou PNG, max 5 MB>

→ {
    "success": true,
    "data": {
      "order_id": 42,
      "payment_status": "proof_submitted",
      "message": "Preuve de paiement reçue. L'admin va vérifier et confirmer votre commande."
    }
  }
```

**Après upload :**
- L'admin reçoit un email de notification automatique
- Il vérifie la preuve dans l'admin Django et met à jour `payment_status` → `verified` puis `paid`
- Le client peut suivre l'état via `GET /api/orders/{id}/` (champ `payment_status`)

---

## Avis — `/api/reviews/`

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/reviews/?product={id}` | Public | Avis d'un produit |
| POST | `/reviews/` | Requis + achat vérifié | Laisser un avis |
| PATCH | `/reviews/{id}/` | Propriétaire | Modifier son avis |
| DELETE | `/reviews/{id}/` | Propriétaire | Supprimer son avis |

---

## Favoris — `/api/wishlist/`

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/wishlist/` | Requis | Liste des favoris |
| POST | `/wishlist/add/` | Requis | Ajouter aux favoris |
| DELETE | `/wishlist/remove/{id}/` | Requis | Retirer des favoris |

---

## Adresses — `/api/addresses/`

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/addresses/` | Requis | Liste des adresses |
| POST | `/addresses/` | Requis | Ajouter une adresse |
| PATCH | `/addresses/{id}/` | Requis | Modifier une adresse |
| DELETE | `/addresses/{id}/` | Requis | Supprimer une adresse |
| PATCH | `/addresses/{id}/default/` | Requis | Définir par défaut |

**Types d'adresse :** `billing` · `shipping`

---

## Communauté — `/api/community/`

Espace communautaire type « groupe » : plusieurs salons thématiques, lecture publique
(selon le salon), écriture réservée aux membres connectés, modération admin, tag produit,
images et réactions. La mise à jour temps réel se fait par **polling** (`?after=`).

**Salons & messages**

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/community/channels/` | Public* | Liste des salons lisibles (+ `can_write`, `is_following`) |
| GET | `/community/channels/{slug}/messages/` | Public* | Messages d'un salon (polling / historique) |
| POST | `/community/channels/{slug}/messages/` | Requis + écriture | Publier un message (multipart) |
| POST | `/community/channels/{slug}/subscribe/` | Requis | Suivre / ne plus suivre un salon (toggle) |
| POST | `/community/messages/{id}/react/` | Requis | Réagir à un message (toggle) |
| DELETE | `/community/messages/{id}/` | Propriétaire ou admin | Supprimer un message (suppression douce) |
| POST | `/community/messages/{id}/` | Admin | Épingler / désépingler un message |
| GET | `/community/users/search/?q=` | Requis | Rechercher des utilisateurs (autocomplete @mention) |

**Notifications**

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/community/notifications/` | Requis | Mes notifications + nombre de non-lus |
| POST | `/community/notifications/` | Requis | Marquer comme lues (toutes, ou `id` précis) |

**Support privé (client ↔ équipe admin)**

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/community/support/messages/` | Requis | Ma conversation avec le support (polling) |
| POST | `/community/support/messages/` | Requis (client) | Envoyer un message au support (multipart) |
| GET | `/community/support/inbox/` | Admin | Liste des conversations clients |
| GET | `/community/support/inbox/{id}/messages/` | Admin | Messages d'une conversation |
| POST | `/community/support/inbox/{id}/messages/` | Admin | Répondre au client (multipart) |

**Modération (admin — `is_staff`)**

| Méthode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| POST | `/community/messages/{id}/ban-author/` | Admin | Bannir / débannir l'auteur (toggle) |
| POST | `/community/messages/{id}/mute-author/` | Admin | Mute / unmute l'auteur dans ce salon (toggle) |
| POST | `/community/channels/{slug}/lock/` | Admin | Cycle d'accès écriture (ouvert → verrouillé → admins) |
| GET / POST | `/community/manage/channels/` | Admin | Lister tous les salons / créer un salon |
| PATCH | `/community/manage/channels/{slug}/` | Admin | Modifier un salon |

> \* « Public » dépend de l'`read_access` du salon. Un salon `public` est lisible sans
> token ; `authenticated` exige un token ; `closed` est réservé aux admins.

### Récupérer les messages (polling)

```
GET /api/community/channels/general/messages/?after=1240

→ {
    "success": true,
    "results": [ { ...message... } ],
    "last_id": 1247
  }
```

- `?after={id}` — renvoie les messages **plus récents** que `{id}` (boucle de polling).
- `?before={id}` — renvoie la page de messages **plus anciens** (remontée d'historique).
- Sans paramètre — renvoie les 30 derniers messages, ordre chronologique.

Boucle conseillée : charger une première page, mémoriser `last_id`, puis interroger
`?after=last_id` toutes les 3–5 s.

### Publier un message

```
POST /api/community/channels/general/messages/
Content-Type: multipart/form-data
Authorization: Bearer <token>

content      (string)   — texte du message (≤ 2000 caractères)
product_id   (int)      — optionnel : produit tagué
reply_to     (int)      — optionnel : ID du message auquel on répond
images       (File[])   — optionnel : jusqu'à 4 images (JPG/PNG/WebP/GIF, ≤ 5 Mo chacune)
```

`content` **ou** au moins une image est obligatoire.

### Objet `message` (réponse)

```json
{
  "id": 1247,
  "channel": 1,
  "author": 12,
  "author_name": "Marie L.",
  "is_staff": false,
  "content": "Ce gâteau était parfait 🎂",
  "created_at": "2026-06-13T14:32:00Z",
  "is_pinned": false,
  "is_deleted": false,
  "product": {
    "id": 8, "name": "Gâteau au chocolat", "slug": "gateau-chocolat",
    "image": "https://.../media/product_images/...jpg", "price": "1 500,00 HTG"
  },
  "reply_to": { "id": 1240, "author": "Jean P.", "excerpt": "Quel parfum ?" },
  "attachments": ["https://.../media/community/attachments/...jpg"],
  "reactions": { "❤️": 4, "🔥": 2 },
  "my_reactions": ["❤️"],
  "is_own": false,
  "can_moderate": false
}
```

Un message supprimé est renvoyé avec `is_deleted: true` et un `content` neutre
(« Message supprimé par la modération. ») ; les autres champs sont vidés.

### Réagir à un message

```
POST /api/community/messages/1247/react/
{ "emoji": "❤️" }

→ { "success": true, "reactions": { "❤️": 5 }, "active": true, "emoji": "❤️" }
```

L'action est un **toggle** : un second appel avec le même émoji retire la réaction.
Émojis autorisés : `❤️` · `😋` · `🔥` · `👍` · `🎂` · `😮`.

### Objet `channel` (réponse `/channels/`)

```json
{
  "id": 1, "name": "Général", "slug": "general",
  "description": "Discussions ouvertes de la communauté.",
  "emoji": "💬", "color": "#C62828", "image": null,
  "read_access": "public", "write_access": "open",
  "can_write": true, "is_following": false
}
```

- `can_write` — false si non connecté, banni, mute, ou salon verrouillé. À utiliser pour activer/désactiver le champ de saisie.
- `is_following` — l'appelant suit-il ce salon (état du bouton 🔔). Bascule via `subscribe/`.

### Suivre un salon & mentions

```
POST /api/community/channels/general/subscribe/
→ { "success": true, "following": true }   // toggle

GET /api/community/users/search/?q=mar
→ { "success": true, "results": [ { "id": 12, "username": "marie", "name": "Marie L." } ] }
```

On suit automatiquement un salon dès qu'on y poste. Mentionner quelqu'un = écrire
`@username` dans le `content` (résolu côté serveur, déclenche une notification).

### Notifications

```
GET /api/community/notifications/
→ {
    "success": true,
    "unread": 3,
    "results": [
      { "id": 90, "type": "mention", "text": "Marie L. vous a mentionné",
        "url": "/community/c/general/", "emoji": "🔔", "count": 1,
        "is_read": false, "created_at": "..." },
      { "id": 88, "type": "support", "text": "L'équipe Hayiti's vous a répondu", ... }
    ]
  }

POST /api/community/notifications/          // marquer tout lu
POST /api/community/notifications/ { "id": 90 }   // marquer une seule
```

`type` ∈ `reply` · `mention` · `channel_message` · `support`. Utile pour router
l'utilisateur (deep-link) à l'ouverture.

### Support privé

Conversation 1-to-1 entre un client et **l'équipe** (inbox partagée : n'importe quel
admin répond). Même moteur que le chat (polling `?after=`, images multipart).

```
# Client
GET  /api/community/support/messages/                 → { success, results:[…], last_id }
POST /api/community/support/messages/  (multipart)    content, images[]

# Admin
GET  /api/community/support/inbox/?q=marie
  → { success, results:[ { id, client_name, unread_count, last_message, last_at } ] }
GET  /api/community/support/inbox/42/messages/        → messages de la conversation 42
POST /api/community/support/inbox/42/messages/  (multipart)   → répond au client
```

Objet message support : `{ id, is_admin, sender, content, attachments[], created_at, is_own }`.

### Modération (admin)

```
POST /api/community/messages/1247/ban-author/   → { success, banned: true,  user: "bob" }
POST /api/community/messages/1247/mute-author/  → { success, muted: true,   user: "bob" }
POST /api/community/channels/general/lock/      → { success, write_access: "locked", label: "Verrouillé — lecture seule" }

GET  /api/community/manage/channels/            → liste complète (salons inactifs inclus)
POST /api/community/manage/channels/            { name, emoji, description, read_access, write_access, is_active }
PATCH /api/community/manage/channels/general/   { write_access: "admins" }
```

Tous ces endpoints exigent `is_staff` (sinon `403 PERMISSION_DENIED`). `ban` et `mute`
sont des **toggles**. Une écriture refusée pour un membre renvoie `403` avec un
`message` explicite (« Vous avez été banni… », « Ce salon est en lecture seule… »).

### Notifications push (FCM)

L'app enregistre son token via `POST /api/auth/fcm-token/`. Les notifications
communauté/support sont envoyées avec un `data` exploitable pour le deep-linking :

```json
{ "type": "mention", "channel": "general", "message_id": "1247" }
{ "type": "support", "conversation": "42" }
```

---

## Back Office Admin — `/api/admin/`

> Tous ces endpoints requièrent `is_staff = True`

### Dashboard
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/admin/dashboard/` | Stats : commandes, revenus, clients, top produits, graphe 30j |

### Produits
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/admin/products/` | Liste complète avec filtres |
| POST | `/admin/products/` | Créer un produit |
| PATCH | `/admin/products/{id}/` | Modifier un produit |
| DELETE | `/admin/products/{id}/` | Supprimer un produit |
| POST | `/admin/products/{id}/images/` | Uploader des images |

### Commandes
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/admin/orders/` | Toutes les commandes + filtres |
| GET | `/admin/orders/{id}/` | Détail complet (inclut `payment_proof_url` et `payment_status`) |
| PATCH | `/admin/orders/{id}/status/` | Changer le statut de livraison (déclenche email) |

### Clients
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/admin/customers/` | Liste des clients |
| GET | `/admin/customers/{id}/` | Profil + historique commandes |
| PATCH | `/admin/customers/{id}/` | Modifier un client |

### Catégories
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/admin/categories/` | Liste |
| POST | `/admin/categories/` | Créer |
| PATCH | `/admin/categories/{id}/` | Modifier |
| DELETE | `/admin/categories/{id}/` | Supprimer |

### Inventaire
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/admin/inventory/` | Produits stock faible (`?threshold=10`) |
| PATCH | `/admin/inventory/{id}/` | Mettre à jour le stock |

### Rapports
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/admin/reports/sales/` | Ventes par période (`?period=daily\|weekly\|monthly&start=&end=`) |
| GET | `/admin/reports/products/` | Produits les plus vendus |
| GET | `/admin/reports/customers/` | Meilleurs clients |

---

## Codes d'erreur

| Code | Statut HTTP | Description |
|------|-------------|-------------|
| `OUT_OF_STOCK` | 409 | Produit épuisé |
| `INSUFFICIENT_STOCK` | 409 | Quantité demandée > stock disponible |
| `ORDER_NOT_CANCELLABLE` | 409 | Commande non annulable (déjà traitée) |
| `PAYMENT_FAILED` | 402 | Échec du paiement |
| `INVALID_PAYMENT_METHOD` | 400 | Méthode de paiement incompatible avec cette action |
| `MISSING_FILE` | 400 | Aucun fichier fourni |
| `INVALID_CREDENTIALS` | 401 | Identifiants incorrects |
| `TOKEN_EXPIRED` | 401 | Token JWT expiré |
| `PERMISSION_DENIED` | 403 | Accès non autorisé |

---

## Notes de migration — Paiement Hors Ligne

> Cette section est destinée à l'équipe Flutter. Elle détaille les changements introduits lors de l'ajout du support offline et ce qu'il faut ajuster dans le code de l'application existante.

---

### Ce qui a changé dans les réponses existantes

Deux nouveaux champs apparaissent désormais dans **toutes** les réponses `Order` (client et admin), y compris les commandes MonCash/Stripe/NatCash déjà existantes :

| Champ | Type | Valeur par défaut | Description |
|-------|------|-------------------|-------------|
| `payment_status` | `string` | `"unpaid"` | État du paiement hors ligne |
| `payment_proof_url` | `string \| null` | `null` | URL absolue de la preuve uploadée |

Ces champs sont **additifs** — ils n'en remplacent aucun. Si ton modèle Freezed utilise `unknownEnumValue` ou `@JsonKey(includeIfNull: false)`, tu n'auras pas d'erreur à la désérialisation, mais tu dois quand même ajouter les champs pour pouvoir les utiliser.

---

### Modèle Dart `Order` — champs à ajouter

```dart
@freezed
class Order with _$Order {
  const factory Order({
    required int id,
    // ... champs existants ...
    required String paymentMethod,
    required String paymentStatus,      // NOUVEAU — 'unpaid' | 'proof_submitted' | 'verified' | 'paid'
    String? paymentProofUrl,            // NOUVEAU — null si pas encore soumise
    required String status,
    // ...
  }) = _Order;

  factory Order.fromJson(Map<String, dynamic> json) => _$OrderFromJson(json);
}
```

Mapping JSON (snake_case → camelCase avec `json_serializable`) :
```dart
@JsonKey(name: 'payment_status')  required String paymentStatus,
@JsonKey(name: 'payment_proof_url') String? paymentProofUrl,
```

---

### Enum `PaymentMethod` — valeur à ajouter

Si tu as un enum côté Flutter pour les méthodes de paiement :

```dart
enum PaymentMethod {
  moncash,
  natcash,
  stripe,
  offline,   // NOUVEAU
}
```

Sans cette valeur, `json_serializable` lèvera une erreur si l'API retourne `"offline"` et que l'enum ne le connaît pas. Ajoute `unknownEnumValue: PaymentMethod.offline` en attendant ou directement la valeur.

---

### Nouveau endpoint à implémenter

```
POST /api/payments/offline/
Content-Type: multipart/form-data
Authorization: Bearer <token>

Champs :
  order_id       (int)   — ID de la commande
  payment_proof  (File)  — Image JPG ou PNG, max 5 MB
```

Exemple avec Dio :

```dart
Future<void> submitPaymentProof(int orderId, File proofFile) async {
  final formData = FormData.fromMap({
    'order_id': orderId,
    'payment_proof': await MultipartFile.fromFile(
      proofFile.path,
      filename: 'proof.jpg',
      contentType: DioMediaType('image', 'jpeg'),
    ),
  });

  final response = await dio.post(
    '/api/payments/offline/',
    data: formData,
  );

  // Réponse attendue :
  // { "success": true, "data": { "order_id": 42, "payment_status": "proof_submitted", ... } }
}
```

---

### Ce qui ne change pas

- Tous les endpoints existants (`/auth/`, `/products/`, `/cart/`, `/orders/`, `/payments/initiate/`, `/payments/verify/`, etc.) fonctionnent exactement comme avant
- Le champ `is_paid` reste présent et inchangé
- Les webhooks MonCash et Stripe sont inchangés
- Les tokens JWT, leur durée et leur rotation sont inchangés

---

## Tokens JWT

| Token | Durée | Paramètre `.env` |
|-------|-------|-----------------|
| Access | 1 jour | `JWT_ACCESS_TOKEN_LIFETIME_DAYS` |
| Refresh | 30 jours | `JWT_REFRESH_TOKEN_LIFETIME_DAYS` |

Les refresh tokens sont **blacklistés** après rotation.
