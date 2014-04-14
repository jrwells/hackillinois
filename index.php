<?php
error_reporting(E_ALL); ini_set('display_errors', 1);

$db = new mysqli(
	'localhost',
	'colorap5_unclec',
	'zLoV$&mF*M#w',
	'colorap5_unclec');

$openingDay = mktime(0, 0, 0, 3, 31, 2014);
$today = strtotime('today midnight');
$yesterday = $today - 86400;
$tomorrow = $today + 86400;

if(isset($_GET['teaser'])) {
	$data_mode = 'teaser_text';
	$link_addition = '&teaser';
}

else {
	$data_mode = 'full_summary';
	$link_addition = '';
}

if(isset($_GET['date'])) {
	$requestedDate = strtotime($_GET['date']);

	if($requestedDate < $openingDay) {
		$requestedDate = $openingDay;
	}

	else if($requestedDate > $today) {
		$requestedDate = $today;
	}

	$queryTimeMySQL = date('Y-m-d H:i:s', $requestedDate);
}

else {
	$requestedDate = $today;
	$queryTimeMySQL = date('Y-m-d H:i:s', $today);
}

$listQuery = 'SELECT `start_time`, `' . $data_mode . '` FROM `games` WHERE `start_time` > "' . $queryTimeMySQL . '" AND `start_time` < DATE_ADD("' . $queryTimeMySQL . '", INTERVAL 24 HOUR) AND `finished` = 1 ORDER BY `start_time` DESC;';

$feed = '';
if($result = $db->query($listQuery)) {
	while($row = $result->fetch_assoc()) {
		$gametime = strtotime($row['start_time']);
		$gametimeString = date("g:ia", $gametime);

		$feed .= '<div class="meta col-md-1"><p>' . $gametimeString . "</p></div>\n";

		$feed .= '<div class="game col-md-10 col-md-offset-1">' . "\n";
		$feed .= '<h2>' . $row[$data_mode] . "</h2><br />\n";
		$feed .= "</div>\n";
	}

	if(!strlen($feed)) {
		$feed .= '<p class="lead">No games have finished yet... check back later!</p>';
	}
}

// build date header with a few special labeled days
$date = date("n/j/Y", $requestedDate);

if($requestedDate == $today) {
	$extra = 'Today';
}

else if($requestedDate == $yesterday) {
	$extra = 'Yesterday';
}

else if($requestedDate == $tomorrow) {
	$extra = 'Tomorrow';
}

else if($requestedDate == $openingDay) {
	$extra = 'Opening Day 2014';
}

else {
	$extra = '';
}

if(strlen($extra)) {
	$date .= "<br><small>$extra</small>";
}

// generate time pagination links
$prev_link = '/unclec/?date=' . date('n/j/Y', $requestedDate - 86400) . $link_addition;
$next_link = '/unclec/?date=' . date('n/j/Y', $requestedDate + 86400) . $link_addition;

// show how many games are left today (if we're looking at today)
if($requestedDate == $today) {
	$remainingQuery = 'SELECT COUNT(1) FROM `games` WHERE `start_time` > DATE_SUB(NOW(), INTERVAL 3 HOUR) AND `finished` = 0;';
	if($result = $db->query($remainingQuery)) {
		$row = $result->fetch_row();
		$s = ($row[0] == 1) ? '' : 's';

		$amount = $row[0];
		$isOrAre = 'are';

		if($amount == 0) {
			$amount = "No";
		}

		else if($amount == 1) {
			$amount = "One";
			$isOrAre = 'is';
		}

		$feed .= '<div class="clearfix"></div>';
		$feed .= "<h1 class=\"moregames\"><small>There $isOrAre $amount game$s left today.</small></h1>";
	}
}

// funtimes
$houses = [
	'Funhouse',
	'Secret Cove',
	'Housebus',
	'Candy Van',
	'Touching Game',
	'Lap',
	'Magical Place',
	'Sports Dungeon',
	'Bouncy Castle',
	];
$house = $houses[array_rand($houses, 1)];
?><!doctype html>
<html lang="en">
<head>
	<title>Bunt.ly</title>
	<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
	<script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
	<link rel="stylesheet" href="style.css">
</head>
<body>
	<div class="container">
		<div class="row top">
			<div class="col-md-4" style="text-align: right">
				<? if($requestedDate != $openingDay): ?>
				<a href="<?= $prev_link; ?>">
					<button type="button" class="btn btn-default">
						<span class="glyphicon glyphicon-chevron-left"></span>
					</button>
				</a>
				<? endif; ?>
			</div>
			<div class="col-md-4" style="text-align: center">
				<h2><?= $date; ?></h2>
			</div>
			<div class="col-md-4" style="text-align: left">
				<? if($requestedDate != $today): ?>
				<a href="<?= $next_link; ?>">
					<button type="button" class="btn btn-default">
						<span class="glyphicon glyphicon-chevron-right"></span>
					</button>
				</a>
				<? endif; ?>
			</div>
		</div>
		<div class="clearfix"></div>
		<?= $feed; ?>
	</div>
</body>
</html>