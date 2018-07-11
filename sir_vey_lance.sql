-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 10, 2018 at 10:11 AM
-- Server version: 10.1.30-MariaDB
-- PHP Version: 7.2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sir_vey_lance`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_user_action` (IN `user_id` INT, IN `action_id` INT)  NO SQL
DELETE FROM user_settings WHERE user_settings.userID = user_id AND user_settings.actionID = action_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `post_summary` (IN `user_id` INT, IN `action_id` INT, IN `start_t` INT, IN `end_t` INT, IN `global_t` VARCHAR(22))  NO SQL
INSERT INTO `surv_summary`(`userID`, `actionID`, `start`, `end`, `gt`) SELECT user_id,action_id,start_t,end_t, global_t WHERE EXISTS(SELECT * FROM `user_settings` WHERE `user_settings`.`userID` = user_id AND `user_settings`.`actionID` = action_id)$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `post_user` (IN `name` VARCHAR(32), IN `token` VARCHAR(64))  NO SQL
INSERT INTO users(Name, Token) VALUES (name,token)$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `post_user_action` (IN `user_id` INT, IN `action_id` INT)  NO SQL
INSERT INTO user_settings(userID, actionID) 
SELECT user_id, action_id FROM actions, users WHERE actions.ID = action_id AND users.ID = user_id$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `actions`
--

CREATE TABLE `actions` (
  `ID` int(11) NOT NULL,
  `Name` varchar(16) COLLATE utf16_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_unicode_ci;

--
-- Dumping data for table `actions`
--

INSERT INTO `actions` (`ID`, `Name`) VALUES
(1, 'Luggage'),
(2, 'Parking'),
(3, 'Crowd'),
(4, 'Weapons'),
(5, 'Fire'),
(6, 'Smoke');

-- --------------------------------------------------------

--
-- Table structure for table `surv_summary`
--

CREATE TABLE `surv_summary` (
  `userID` int(11) NOT NULL,
  `actionID` int(11) NOT NULL,
  `start` int(10) UNSIGNED NOT NULL,
  `end` int(11) NOT NULL,
  `gt` varchar(21) CHARACTER SET utf8 COLLATE utf8_unicode_520_ci NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_unicode_ci;

--
-- Dumping data for table `surv_summary`
--

INSERT INTO `surv_summary` (`userID`, `actionID`, `start`, `end`, `gt`, `id`) VALUES
(147, 1, 15, 0, '2018-7-4-23-37-28', 30),
(147, 1, 16, 25, '2018-7-4-23-37-28', 31),
(147, 3, 18, 20, '2018-7-4-23-37-28', 32),
(147, 4, 19, 20, '2018-7-4-23-37-28', 33),
(147, 6, 19, 20, '2018-7-4-23-37-28', 34),
(146, 1, 10, 15, '2018-7-5-2-44-48', 42),
(146, 3, 12, 18, '2018-7-5-2-44-48', 43),
(146, 4, 15, 20, '2018-7-5-2-44-48', 44),
(146, 6, 112, 115, '2018-7-5-2-44-48', 45),
(146, 4, 2, 0, '2018-7-5-4-45-35', 46),
(146, 4, 2, 0, '2018-7-5-4-45-35', 47),
(146, 4, 2, 0, '2018-7-5-4-45-35', 48),
(146, 4, 2, 0, '2018-7-5-4-45-35', 49),
(146, 4, 2, 0, '2018-7-5-4-45-35', 50),
(146, 4, 2, 0, '2018-7-5-4-45-35', 51),
(146, 4, 2, 0, '2018-7-5-4-45-35', 52),
(146, 4, 2, 0, '2018-7-5-4-45-35', 53),
(146, 4, 2, 0, '2018-7-5-4-45-35', 54),
(146, 4, 2, 0, '2018-7-5-4-45-35', 55),
(146, 4, 2, 0, '2018-7-5-4-45-35', 56),
(146, 4, 2, 0, '2018-7-5-4-45-35', 57),
(146, 4, 2, 0, '2018-7-5-4-45-35', 58),
(146, 4, 2, 0, '2018-7-5-4-45-35', 59),
(146, 4, 2, 0, '2018-7-5-4-45-35', 60),
(146, 4, 2, 0, '2018-7-5-4-45-35', 61);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `Name` varchar(32) COLLATE utf16_unicode_ci NOT NULL,
  `Token` varchar(64) COLLATE utf16_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `Name`, `Token`) VALUES
(146, 'a@a', '02f5f6b6eed9215e6cb9e081a844ff75'),
(147, 'test@test.com', '529c36ae55d40c7381aa0bfe40f23e86'),
(148, 'gc@gv', 'dc061825f8e33c1f92443b7dbcbc4ada');

-- --------------------------------------------------------

--
-- Table structure for table `user_settings`
--

CREATE TABLE `user_settings` (
  `userID` int(11) NOT NULL,
  `actionID` int(11) NOT NULL,
  `extra_info` int(11) NOT NULL DEFAULT '4'
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_unicode_ci;

--
-- Dumping data for table `user_settings`
--

INSERT INTO `user_settings` (`userID`, `actionID`, `extra_info`) VALUES
(137, 6, 4),
(138, 2, 4),
(138, 4, 4),
(138, 6, 4),
(139, 4, 4),
(139, 6, 4),
(141, 3, 4),
(142, 1, 4),
(142, 6, 4),
(143, 1, 4),
(143, 3, 4),
(144, 1, 4),
(144, 3, 4),
(144, 5, 4),
(146, 1, 4),
(146, 3, 1),
(146, 4, 4),
(147, 1, 4),
(147, 4, 4),
(149, 1, 4),
(151, 2, 4),
(151, 3, 4),
(151, 4, 4),
(152, 2, 4),
(153, 2, 4),
(153, 3, 2),
(154, 2, 6),
(154, 3, 1),
(154, 4, 4),
(155, 4, 4),
(155, 5, 4),
(161, 3, 4),
(161, 4, 4),
(161, 5, 4),
(163, 4, 4),
(164, 1, 4),
(164, 3, 1),
(164, 4, 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `actions`
--
ALTER TABLE `actions`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `surv_summary`
--
ALTER TABLE `surv_summary`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userID` (`userID`),
  ADD KEY `actionID` (`actionID`);
ALTER TABLE `surv_summary` ADD FULLTEXT KEY `gt` (`gt`);
ALTER TABLE `surv_summary` ADD FULLTEXT KEY `gt_2` (`gt`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `user_settings`
--
ALTER TABLE `user_settings`
  ADD PRIMARY KEY (`userID`,`actionID`),
  ADD KEY `userID` (`userID`),
  ADD KEY `actionID` (`actionID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `actions`
--
ALTER TABLE `actions`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `surv_summary`
--
ALTER TABLE `surv_summary`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=149;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `surv_summary`
--
ALTER TABLE `surv_summary`
  ADD CONSTRAINT `surv_summary_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`ID`),
  ADD CONSTRAINT `surv_summary_ibfk_2` FOREIGN KEY (`actionID`) REFERENCES `actions` (`ID`);

--
-- Constraints for table `user_settings`
--
ALTER TABLE `user_settings`
  ADD CONSTRAINT `user_settings_ibfk_1` FOREIGN KEY (`actionID`) REFERENCES `actions` (`ID`),
  ADD CONSTRAINT `user_settings_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `users` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
