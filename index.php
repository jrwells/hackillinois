<?php
error_reporting(E_ALL); ini_set('display_errors', 1);

$db = new mysqli(
	'localhost',
	'colorap5_unclec',
	'zLoV$&mF*M#w',
	'colorap5_unclec');

if(isset($_GET['reset'])) {
	$resetQuery = 'UPDATE `games` SET `finished` = 0;';
	$db->query($resetQuery);

	// exec('python update_parser.py');
}

$listQuery = 'SELECT `full_summary` FROM `games` WHERE `start_time` < NOW() AND `finished` = 1;';

$feed = '';
if($result = $db->query($listQuery)) {
	while($row = $result->fetch_assoc()) {
		$feed .= '<h2>' . $row['full_summary'] . '</h2><br />';
	}
}
?><!doctype html>
<html lang="en">
<head>
	<title>Uncle Charlie's Funhouse</title>
	<style type="text/css">
	body {
		padding-top: 10%;
	}
	</style>
	<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
	<script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
</head>
<body>
	<div class="container">
		<?= $feed; ?>
	</div>
</body>
</html>