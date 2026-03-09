PRAGMA foreign_keys = ON;

INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin,
    created_at,
    updated_at
) VALUES (
    '11111111-1111-1111-1111-111111111111',
    'Admin',
    'User',
    'admin@hbnb.io',
    '$2b$12$abcdefghijklmnopqrstuvABCDEFGHIJKLMNOpqrstuvwxyz123456',
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO amenities (
    id,
    name,
    description,
    created_at,
    updated_at
) VALUES
(
    '33333333-3333-3333-3333-333333333331',
    'WiFi',
    'High-speed wireless internet',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),
(
    '33333333-3333-3333-3333-333333333332',
    'Swimming Pool',
    'Outdoor swimming pool',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),
(
    '33333333-3333-3333-3333-333333333333',
    'Air Conditioning',
    'Cooling and heating system',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
