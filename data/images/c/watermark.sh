#!/bin/bash

mv $1 $1-orig
composite -gravity southeast -quality 100 \( sig9642.png \) $1-orig $1
