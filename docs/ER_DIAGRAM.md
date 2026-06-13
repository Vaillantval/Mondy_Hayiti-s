# Schéma Entité-Relation — Hayiti's

Diagramme ER de l'ensemble des modèles de données du projet, généré à partir des
modèles Django (`accounts`, `dashboard`, `shop`, `api`).

> Rendu automatique sur GitHub, dans la plupart des IDE et sur https://mermaid.live

## Diagramme complet

```mermaid
erDiagram
    %% ───────────────── COMPTES & ADRESSES ─────────────────
    Customer ||--o{ Adress       : "possède"
    Customer ||--o{ Order        : "passe (PROTECT)"
    Customer ||--o{ CartItem     : "a dans son panier"
    Customer ||--o{ Review       : "rédige"
    Customer ||--o{ WishlistItem : "ajoute aux favoris"

    %% ───────────────── CATALOGUE ─────────────────
    Product  }o--o{ Category     : "classé dans"
    Product  ||--o{ Image        : "illustré par"
    Product  ||--o{ ProductPrice : "variantes de prix"
    Product  ||--o{ CartItem     : "référencé par"
    Product  ||--o{ Review       : "évalué par"
    Product  ||--o{ WishlistItem : "mis en favori"
    Product  |o--o{ OrderDetail  : "commandé via (SET_NULL)"

    %% ───────────────── COMMANDES ─────────────────
    Order    ||--o{ OrderDetail  : "détaillée par"

    Customer {
        int      id PK
        string   username UK
        string   email
        string   password
        string   first_name
        string   last_name
        bool     is_staff
        bool     is_active
        bool     agree_terms
        string   phone
        string   fcm_token "token push Firebase"
        datetime date_joined
    }

    Adress {
        int      id PK
        int      author_id FK "Customer (CASCADE)"
        string   name
        string   full_name
        string   street
        string   code_postal
        string   city
        string   country
        string   phone
        text     more_details
        string   adress_type "billing|shipping"
        bool     is_default
        datetime created_at
        datetime updated_at
    }

    Category {
        int      id PK
        string   name
        string   description
        slug     slug
        bool     is_mega
        image    image
        datetime created_at
        datetime updated_at
    }

    Product {
        int      id PK
        string   name
        slug     slug UK
        string   description
        text     more_description
        string   additional_info
        int      stock
        float    solde_price
        float    regular_price
        string   brand
        bool     is_available
        bool     is_best_seller
        bool     is_featured
        bool     is_new_arrival
        bool     is_special_offer
        datetime created_at
        datetime updated_at
    }

    ProductPrice {
        int      id PK
        int      product_id FK "Product (CASCADE)"
        string   label
        float    price
        float    regular_price
        int      order
    }

    Image {
        int      id PK
        int      product_id FK "Product (CASCADE)"
        image    image
        datetime created_at
        datetime updated_at
    }

    Order {
        int      id PK
        int      author_id FK "Customer (PROTECT)"
        string   client_name
        string   billing_address
        string   shipping_address
        int      quantity
        float    taxe
        float    order_cost "HT"
        float    order_cost_ttc "TTC"
        bool     is_paid
        string   carrier_name "snapshot"
        float    carrier_price "snapshot"
        string   payment_method
        string   stripe_payment_intent
        image    payment_proof "preuve hors ligne"
        string   payment_status "unpaid|proof_submitted|verified|paid"
        string   status "pending|processing|shipped|delivered|canceled"
        datetime created_at
        datetime updated_at
    }

    OrderDetail {
        int      id PK
        int      order_id FK "Order (CASCADE)"
        int      product_id FK "Product (SET_NULL)"
        string   product_name "snapshot"
        text     product_description "snapshot"
        float    solde_price "snapshot"
        float    regular_price "snapshot"
        int      quantity
        float    taxe
        float    sub_total_ht
        float    sub_total_ttc
        datetime created_at
        datetime updated_at
    }

    CartItem {
        int      id PK
        int      user_id FK "Customer (CASCADE)"
        int      product_id FK "Product (CASCADE)"
        int      quantity
        datetime created_at
        datetime updated_at
    }

    Review {
        int      id PK
        int      product_id FK "Product (CASCADE)"
        int      author_id FK "Customer (CASCADE)"
        int      rating "1..5"
        text     comment
        datetime created_at
        datetime updated_at
    }

    WishlistItem {
        int      id PK
        int      user_id FK "Customer (CASCADE)"
        int      product_id FK "Product (CASCADE)"
        datetime created_at
    }
```

> **Contraintes d'unicité (`unique_together`)** non représentables en arêtes Mermaid :
> `CartItem(user, product)`, `Review(product, author)`, `WishlistItem(user, product)`,
> `ExchangeRate(base_currency, target_currency)`.

## Tables autonomes (sans clé étrangère)

Modèles de configuration et de contenu éditorial, non reliés au reste du graphe.

```mermaid
erDiagram
    Setting {
        int      id PK
        string   name
        text     description
        string   base_currency "devise de saisie"
        string   currency "devise d'affichage"
        float    taxe_rate
        image    logo
        string   street
        string   city
        string   state
        string   code_postal
        string   phone
        email    email
        text     copyright
        bool     show_app_banner
        file     apk_file ".apk Android"
        string   apk_version
        string   apk_description
        datetime created_at
        datetime updated_at
    }

    ExchangeRate {
        int      id PK
        string   base_currency
        string   target_currency
        float    rate
        datetime updated_at
    }

    Carrier {
        int      id PK
        string   name
        string   description
        text     details
        float    price
        image    image
        datetime created_at
        datetime updated_at
    }

    Method {
        int      id PK
        string   name
        string   description
        text     more_description
        image    logo
        string   test_public_key
        string   test_private_key
        string   prod_public_key
        string   prod_private_key
        bool     is_available
        datetime created_at
        datetime updated_at
    }

    Slider {
        int      id PK
        string   title
        string   description
        string   button_text
        string   button_link
        image    image
        datetime created_at
        datetime updated_at
    }

    Collection {
        int      id PK
        string   title
        string   description
        string   button_text
        string   button_link
        image    image
        datetime created_at
        datetime updated_at
    }

    Page {
        int      id PK
        string   name
        slug     slug UK
        string   subtitle
        text     content
        image    image
        string   page_type "about|terms|privacy|general"
        bool     is_head
        bool     is_foot
        bool     is_checkout
        datetime created_at
        datetime updated_at
    }

    FAQ {
        int      id PK
        string   question
        text     answer
        int      order
        bool     is_active
        datetime created_at
        datetime updated_at
    }

    ContactMessage {
        int      id PK
        string   name
        email    email
        string   subject
        text     message
        bool     is_read
        datetime created_at
    }
```

## Légende des cardinalités

| Notation Mermaid | Signification                          | Exemple                          |
|------------------|----------------------------------------|----------------------------------|
| `\|\|--o{`       | un-à-plusieurs (0..N)                   | un `Customer` → N `Order`        |
| `\|o--o{`        | un(0..1)-à-plusieurs                    | un `Product` → N `OrderDetail`   |
| `}o--o{`         | plusieurs-à-plusieurs                   | `Product` ↔ `Category`           |

**Conventions de suppression :**
- `CASCADE` — la suppression du parent supprime les enfants (ex. `Image`, `ProductPrice`, `OrderDetail`→`Order`).
- `PROTECT` — empêche la suppression d'un `Customer` ayant des `Order`.
- `SET_NULL` — la suppression d'un `Product` conserve l'`OrderDetail` (historique de commande préservé grâce aux champs dénormalisés `product_name`, `solde_price`…).

---

*Généré à partir des modèles Django du projet Hayiti's. Pour régénérer une image depuis
l'ORM : `python manage.py graph_models accounts shop dashboard api -o er.png`
(nécessite `django-extensions` + Graphviz).*
