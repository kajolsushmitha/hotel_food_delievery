hotel-food-ordering
│
├── backend/
│   │
│   ├── main.py
│   │
│   ├── config.py
│   ├── db.py
│   │
│   ├── model/                 # MODEL
│   │   ├── __init__.py
│   │   ├── hotel_model.py
│   │   ├── menu_model.py
│   │   ├── pass_model.py
│   │   └── order_model.py
│   │
│   ├── schema/                # Request/Response Models
│   │   ├── __init__.py
│   │   ├── hotel_schema.py
│   │   ├── menu_schema.py
│   │   ├── pass_schema.py
│   │   └── order_schema.py
│   │
│   ├── controller/            # CONTROLLER
│   │   ├── __init__.py
│   │   ├── hotel_controller.py
│   │   ├── menu_controller.py
│   │   ├── pass_controller.py
│   │   └── order_controller.py
│   │
│   ├── services/               # BUSINESS LOGIC
│   │   ├── __init__.py
│   │   ├── hotel_services.py
│   │   ├── menu_services.py
│   │   ├── pass_services.py
│   │   └── order_services.py
│   │
│   ├── repository/           # DATABASE OPERATIONS
│   │   ├── __init__.py
│   │   ├── hotel_repository.py
│   │   ├── menu_repository.py
│   │   ├── pass_repository.py
│   │   └── order_repository.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── qr_generator.py
│
├── frontend/
│   ├── index.html
│   ├── menu.html
│   ├── order.html
│   ├── success.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── menu.js
│       └── order.js
│
├── tests/
│   ├── test_hotel.py
│   ├── test_menu.py
│   └── test_order.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
