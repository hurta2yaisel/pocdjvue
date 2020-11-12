-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 10, 2020 at 11:20 AM
-- Server version: 5.5.60-MariaDB
-- PHP Version: 7.1.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `webfactura_prod`
--

-- --------------------------------------------------------

--
-- Table structure for table `bodega`
--

CREATE TABLE `bodega` (
  `id` int(11) NOT NULL,
  `empresa_id` int(11) NOT NULL,
  `usuarioRegistro_id` int(11) DEFAULT NULL,
  `usuarioModifico_id` int(11) DEFAULT NULL,
  `bodegaCodigo` varchar(15) CHARACTER SET utf8 NOT NULL,
  `bodegaNombre` varchar(100) CHARACTER SET utf8 NOT NULL,
  `bodegaDireccion` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `bodegaTelefono` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `bodegaDescripcion` text CHARACTER SET utf8,
  `bodegaRegistro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `bodegaModifico` datetime DEFAULT NULL,
  `bodegaMatriz` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bodega`
--

INSERT INTO `bodega` (`id`, `empresa_id`, `usuarioRegistro_id`, `usuarioModifico_id`, `bodegaCodigo`, `bodegaNombre`, `bodegaDireccion`, `bodegaTelefono`, `bodegaDescripcion`, `bodegaRegistro`, `bodegaModifico`, `bodegaMatriz`) VALUES
(156, 2, NULL, NULL, '85236200-6', 'Bodega Matriz', 'Avda. El Rosal 4571', NULL, 'Bodega principal', '2020-11-10 14:19:20', NULL, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bodega`
--
ALTER TABLE `bodega`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_empresaBodega_id_empresa` (`empresa_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bodega`
--
ALTER TABLE `bodega`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=157;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
