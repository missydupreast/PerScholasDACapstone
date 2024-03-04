-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 20, 2023 at 09:35 AM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 8.0.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Cap_evidence`
--

-- --------------------------------------------------------

--
-- Table structure for table `evidence`
--

CREATE TABLE `evidence` (
  `evidence_id` int(11) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `evidence`
--

INSERT INTO `evidence` (`evidence_id`, `description`) VALUES
(1, 'Document A'),
(2, 'Photograph B'),
(3, 'Document B'),
(4, 'Fingerprint C'),
(5, 'VideoTape D'),
(6, 'Photograph C'),
(7, 'Eyewitness B'),
(8, 'Photograph B'),
(9, 'Audio Recording C'),
(10, 'Voicemail F'),
(11, 'Video Footage F');

-- --------------------------------------------------------

--
-- Table structure for table `evidence_changes`
--

CREATE TABLE `evidence_changes` (
  `change_id` int(11) NOT NULL,
  `evidence_id` int(11) DEFAULT NULL,
  `action` varchar(10) DEFAULT NULL,
  `change_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `evidence`
--
ALTER TABLE `evidence`
  ADD PRIMARY KEY (`evidence_id`);

--
-- Indexes for table `evidence_changes`
--
ALTER TABLE `evidence_changes`
  ADD PRIMARY KEY (`change_id`),
  ADD KEY `evidence_id` (`evidence_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `evidence_changes`
--
ALTER TABLE `evidence_changes`
  MODIFY `change_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `evidence_changes`
--
ALTER TABLE `evidence_changes`
  ADD CONSTRAINT `evidence_changes_ibfk_1` FOREIGN KEY (`evidence_id`) REFERENCES `evidence` (`evidence_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
