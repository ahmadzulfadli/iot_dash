CREATE TABLE `iot_db`.`komposter` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `temperature` FLOAT NOT NULL,
  `moisture` FLOAT NOT NULL,
  `ph_meter` FLOAT NOT NULL,
  `count_day` INT NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;