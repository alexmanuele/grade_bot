#! /bin/bash
`crontab -l > tempfile`
`sed -i '/grades.sh/d' ./tempfile`
`sed -i '/stop.sh/d' ./tempfile`
`crontab -r`
`crontab tempfile`
`rm tempfile`
echo "Removed process from crontab."

