# Hotel Food Ordering - API Documentation

## 1. Passenger Domain (Customer)
- `POST   /passengers`                          -> Register / Create passenger profile (Public)
- `POST   /auth/passenger/login`                -> Login via 10-digit phone number -> Returns Passenger JWT token
- `PATCH  /passengers/{passenger_id}`           -> Update passenger details (Protected: Passenger JWT)
- `DELETE /passengers/{passenger_id}`           -> Delete passenger account (Protected: Passenger JWT)
- `GET    /hotels`                              -> Browse all active hotels (Public)
- `GET    /hotels/{hotel_id}`                   -> View specific hotel profile (Public)
- `GET    /hotels/{hotel_id}/menu`              -> Browse menu items for a hotel (Public)
- `POST   /orders`                              -> Create / Place an order (Public / Customer)
- `GET    /passengers/{passenger_id}/orders`    -> View my order history (Protected: Passenger JWT)

---

## 2. Hotel Admin Domain (Restaurant Management)
- `POST   /auth/hotel/login`                    -> Login via 10-digit hotel phone number -> Returns Hotel JWT token
- `POST   /hotels/{hotel_id}/menu`              -> Add new item to hotel menu (Protected: Hotel JWT)
- `PATCH  /menu/{menu_id}`                      -> Update menu item (Protected: Hotel JWT)
- `DELETE /menu/{menu_id}`                      -> Remove item from menu (Protected: Hotel JWT)
- `GET    /hotels/{hotel_id}/orders`            -> View all incoming orders for this hotel (Protected: Hotel JWT)
- `PATCH  /orders/{order_id}/status`            -> Update order status (Protected: Hotel JWT)
- `GET    /hotels/{hotel_id}/order-history`     -> View order history & analytics (Protected: Hotel JWT)
- `PATCH  /hotels/{hotel_id}`                   -> Update hotel profile details (Protected: Hotel JWT)
- `DELETE /hotels/{hotel_id}`                   -> Delete hotel account (Protected: Hotel JWT)

---

## 3. Platform / Super Admin & System Domain
- `POST   /hotels`                              -> Register new hotel on the platform
- `GET    /passengers`                          -> View all registered passengers (Super Admin)
- `GET    /passengers/{passenger_id}`           -> View passenger profile by ID (Super Admin)
- `GET    /orders/{order_id}`                   -> Track / View single order by ID
- `DELETE /orders/{order_id}`                   -> Delete / Cancel an order
- `DELETE /orders/expired`                      -> TTL cleanup of expired orders (> 30 days)


 
