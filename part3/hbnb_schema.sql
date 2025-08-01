
------------------------------------------------------------

-- ================================================
-- TASK 9 - SQL SCRIPTS FOR HBNB DATABASE
-- ================================================

-- ================================================
-- 1. CREATE TABLES
-- ================================================

-- Table USERS
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,                    -- UUID format
    first_name VARCHAR(50) NOT NULL,            -- Max 50 chars (validation Python)
    last_name VARCHAR(50) NOT NULL,             -- Max 50 chars (validation Python)
    email VARCHAR(255) UNIQUE NOT NULL,         -- Unique email with @ validation
    password VARCHAR(255) NOT NULL,             -- Bcrypt hash storage
    is_admin BOOLEAN DEFAULT FALSE,             -- Admin role flag
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Auto timestamp
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table PLACES  
CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,                    -- UUID format
    title VARCHAR(100) NOT NULL,                -- Max 100 chars (validation Python)
    description TEXT,                           -- Long text description
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),  -- Positive price validation
    latitude FLOAT NOT NULL CHECK (latitude >= -90.0 AND latitude <= 90.0),   -- GPS validation
    longitude FLOAT NOT NULL CHECK (longitude >= -180.0 AND longitude <= 180.0), -- GPS validation
    owner_id CHAR(36) NOT NULL,                 -- Foreign key to users
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table AMENITIES
CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,                    -- UUID format
    name VARCHAR(50) UNIQUE NOT NULL,           -- Max 50 chars, unique name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table REVIEWS
CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,                    -- UUID format
    text TEXT NOT NULL,                         -- Review content (required)
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),  -- Rating 1-5 validation
    user_id CHAR(36) NOT NULL,                  -- Foreign key to users
    place_id CHAR(36) NOT NULL,                 -- Foreign key to places
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    UNIQUE(user_id, place_id)                   -- One review per user per place
);

-- Table PLACE_AMENITIES (Many-to-Many relationship)
CREATE TABLE place_amenities (
    place_id CHAR(36) NOT NULL,                 -- Foreign key to places
    amenity_id CHAR(36) NOT NULL,               -- Foreign key to amenities
    PRIMARY KEY (place_id, amenity_id),         -- Composite primary key
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- ================================================
-- 2. INITIAL DATA INSERTION
-- ================================================

-- Insert Administrator User (Fixed ID as per requirements)
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',    -- Fixed admin ID
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewEyCoUCLl/JR.9.',  -- bcrypt hash of 'admin1234'
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Initial Amenities (Generated UUIDs)
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('550e8400-e29b-41d4-a716-446655440002', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('550e8400-e29b-41d4-a716-446655440003', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- ================================================
-- 3. INDEXES FOR PERFORMANCE
-- ================================================

-- Index on email for faster user lookup
CREATE INDEX idx_users_email ON users(email);

-- Index on owner_id for faster place queries
CREATE INDEX idx_places_owner ON places(owner_id);

-- Index on user_id and place_id for faster review queries  
CREATE INDEX idx_reviews_user ON reviews(user_id);
CREATE INDEX idx_reviews_place ON reviews(place_id);

-- Index on amenity name for faster searches
CREATE INDEX idx_amenities_name ON amenities(name);

-- ================================================
-- 4. CRUD OPERATIONS TESTING
-- ================================================

-- Test 1: CREATE operations
-- Insert a test user
INSERT INTO users (id, first_name, last_name, email, password, is_admin) 
VALUES ('test-uuid-001', 'John', 'Doe', 'john@test.com', 'hashed_password', FALSE);

-- Insert a test place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES ('test-uuid-002', 'Cozy Apartment', 'A nice place to stay', 100.00, 37.7749, -122.4194, 'test-uuid-001');

-- Insert a test review
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES ('test-uuid-003', 'Great place!', 5, 'test-uuid-001', 'test-uuid-002');

-- Link place with amenity
INSERT INTO place_amenities (place_id, amenity_id)
VALUES ('test-uuid-002', '550e8400-e29b-41d4-a716-446655440001');

-- Test 2: READ operations
-- Get all users
SELECT * FROM users;

-- Get places with owner information
SELECT p.title, p.price, u.first_name, u.last_name 
FROM places p 
JOIN users u ON p.owner_id = u.id;

-- Get reviews with user and place information
SELECT r.text, r.rating, u.first_name, p.title
FROM reviews r
JOIN users u ON r.user_id = u.id  
JOIN places p ON r.place_id = p.id;

-- Get places with their amenities
SELECT p.title, a.name
FROM places p
JOIN place_amenities pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id;

-- Test 3: UPDATE operations
-- Update user information
UPDATE users 
SET first_name = 'Jane', updated_at = CURRENT_TIMESTAMP 
WHERE id = 'test-uuid-001';

-- Update place price
UPDATE places 
SET price = 120.00, updated_at = CURRENT_TIMESTAMP 
WHERE id = 'test-uuid-002';

-- Update review rating
UPDATE reviews 
SET rating = 4, updated_at = CURRENT_TIMESTAMP 
WHERE id = 'test-uuid-003';

-- Test 4: DELETE operations
-- Delete review (cascade will handle references)
-- DELETE FROM reviews WHERE id = 'test-uuid-003';

-- Delete place (cascade will handle reviews and amenity links)
-- DELETE FROM places WHERE id = 'test-uuid-002';

-- Delete user (cascade will handle places and reviews)
-- DELETE FROM users WHERE id = 'test-uuid-001';

-- ================================================
-- 5. DATA INTEGRITY VERIFICATION
-- ================================================

-- Verify foreign key constraints
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
WHERE REFERENCED_TABLE_NAME IS NOT NULL
AND TABLE_SCHEMA = DATABASE();

-- Verify unique constraints
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu 
ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
WHERE tc.CONSTRAINT_TYPE = 'UNIQUE'
AND tc.TABLE_SCHEMA = DATABASE();

-- Verify admin user exists
SELECT id, email, is_admin FROM users WHERE is_admin = TRUE;

-- Verify amenities are inserted
SELECT COUNT(*) as amenity_count FROM amenities;

-- ================================================
-- 6. CLEAN UP TEST DATA (Optional)
-- ================================================

-- Remove test data (uncomment to use)
-- DELETE FROM place_amenities WHERE place_id = 'test-uuid-002';
-- DELETE FROM reviews WHERE id = 'test-uuid-003';  
-- DELETE FROM places WHERE id = 'test-uuid-002';
-- DELETE FROM users WHERE id = 'test-uuid-001';
