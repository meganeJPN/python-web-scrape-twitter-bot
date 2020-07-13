CREATE TABLE new_info_in_mori_hp (
    id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255),
    date VARCHAR(255),
    url VARCHAR(255),
    created_at datetime default current_timestamp,
    PRIMARY KEY (id)
);