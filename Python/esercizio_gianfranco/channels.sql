-- Creazione della tabella channels
CREATE TABLE esercizio1.channels (
    channel_id INT PRIMARY KEY,
    channel_desc VARCHAR(50) NOT NULL,
    channel_class VARCHAR(20) NOT NULL,
    channel_class_id INT NOT NULL,
    channel_total VARCHAR(20) NOT NULL,
    channel_total_id INT NOT NULL,
    
    -- Indici per migliorare le performance delle query
    INDEX idx_channel_class (channel_class),
    INDEX idx_channel_class_id (channel_class_id)
);



