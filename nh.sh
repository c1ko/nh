mkdir -p "$HOME/.nh"  # Make sure the base directory exists

echo "$(history)" > "$HOME/.nh/history"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python3 "$DIR/nh.py"
exit_code="$?"
rm "$HOME/.nh/history"

if [ "$exit_code" -eq 11 ] 
then
	python3 "$DIR/nh_edit.py"
	exit_code="$?"
fi

if [ "$exit_code" -eq 10 ]
then
	action="$(cat $HOME/.nh/action)"
	rm "$HOME/.nh/action"
	history -s "$action"
	$action
fi