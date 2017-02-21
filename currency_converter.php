#!/usr/bin/env php
<?php
function convert_currency($amount_string, $conversions) {
    list($currency_type, $number_string) = split(" ", $amount_string);
    $foreign_amount = (float)$number_string;
    $usd = $foreign_amount * $conversions[strtoupper($currency_type)];
    return "USD " . number_format($usd, 2);
}

function show_conversions($amount_strings, $conversions) {
    foreach ($amount_strings as $amount_string) {
        print(strtoupper($amount_string) . " = " .
              convert_currency($amount_string, $conversions) . "\n");
    }
}

$xml = file_get_contents("conversions.xml");
$conversions = array();
$root = new SimpleXMLElement($xml);
foreach ($root->conversion as $conversion) {
    $conversions[(string)$conversion->currency] = (float)$conversion->rate;
}
$currency_args = array_slice($argv, 1);
$amount_strings = array();
foreach(array_chunk($currency_args, 2) as $chunk) {
    $amount_strings[] = join(" ", $chunk);
}
show_conversions($amount_strings, $conversions);
