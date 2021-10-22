CREATE DATABASE MQTT;
-- keine Primary Keys weil unwichtig --
-- man könnte beim ersten Table einen Primary Key einfügen,
-- dann könnte man über die id 120-180 noch schneller filtern --
CREATE TABLE TableBinary(
created_at DATETIME2(7),
received_at DATETIME2(7),
sensor_data BINARY(2048)
)

CREATE TABLE TableDataPackage(
package_id INT,
started_at DATETIME2(7),
created_at DATETIME2(7),
received_at DATETIME2(7),
sensor_data SMALLINT
)