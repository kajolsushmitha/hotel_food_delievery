HOTEL
├── GET    /hotels
├── GET    /hotels/{hotel_id}
├── PATCH  /hotels/{hotel_id}
└── DELETE /hotels/{hotel_id} //tenant


MENU
├── POST   /hotels/{hotel_id}/menu
├── GET    /hotels/{hotel_id}/menu
├── GET    /menu/{menu_id}
├── PATCH  /menu/{menu_id}
└── DELETE /menu/{menu_id}


PASSENGER
├── POST   /passengers
├── GET    /passengers
├── GET    /passengers/{passenger_id}
├── PATCH  /passengers/{passenger_id}
└── DELETE /passengers/{passenger_id}


ORDER
├── POST   /orders
├── GET    /orders
├── GET    /orders/{order_id}
├── GET    /passengers/{passenger_id}/orders
├── GET    /hotels/{hotel_id}/orders
├── PATCH  /orders/{order_id}/status
└── DELETE /orders/{order_id}


PASSENGER AUTHENTICATION (JWT)
├── POST   /auth/passenger/login      (Login via 10-digit phone number -> Returns JWT token)
├── GET    /auth/passenger/me         (Protected: Get current passenger profile)
└── GET    /auth/passenger/orders     (Protected: Get orders for authenticated passenger)


 
