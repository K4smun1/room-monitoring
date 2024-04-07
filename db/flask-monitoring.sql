--
-- Database: `flask-monitoring`
--

-- --------------------------------------------------------

--
-- Table structure for table `data`
--

CREATE TABLE data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gas_an INT,
    gas_di BOOL,
    temp FLOAT,
    hum FLOAT,
    status VARCHAR(30),
    time DATETIME DEFAULT CURRENT_TIMESTAMP
);
