-- Initialize Database
CREATE DATABASE IF NOT EXISTS hotel_food;
USE hotel_food;

-- 1. Hotel Table
CREATE TABLE IF NOT EXISTS hotel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Passenger Table
CREATE TABLE IF NOT EXISTS passenger (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL UNIQUE,
    busNo VARCHAR(50),
    email VARCHAR(255),
    age INT,
    gender VARCHAR(20),
    seatNo INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Menu Item Table
CREATE TABLE IF NOT EXISTS menu_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hotelId INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hotelId) REFERENCES hotel(id) ON DELETE CASCADE
);

-- 4. Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passengerId INT NOT NULL,
    hotelId INT NOT NULL,
    totalAmount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    orderTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (passengerId) REFERENCES passenger(id) ON DELETE CASCADE,
    FOREIGN KEY (hotelId) REFERENCES hotel(id) ON DELETE CASCADE
);

-- 5. Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id VARCHAR(64) PRIMARY KEY,
    orderId INT NOT NULL,
    menuItemId INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (orderId) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menuItemId) REFERENCES menu_item(id) ON DELETE CASCADE
);

-- 6. Hotel Order History Table
CREATE TABLE IF NOT EXISTS hotel_order_history (
    id CHAR(36) NOT NULL,
    hotelId INT NOT NULL,
    passengerId INT NOT NULL,
    orderId INT NOT NULL,
    orderTimestamp BIGINT NOT NULL,
    items JSON NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_order (orderId),
    KEY passengerId (passengerId),
    KEY idx_hotel_timestamp (hotelId, orderTimestamp),
    KEY idx_hotel_passenger_timestamp (
        hotelId,
        passengerId,
        orderTimestamp
    ),
    CONSTRAINT hotel_order_history_ibfk_1
        FOREIGN KEY (hotelId)
        REFERENCES hotel (id),
    CONSTRAINT hotel_order_history_ibfk_2
        FOREIGN KEY (passengerId)
        REFERENCES passenger (id)
) ;