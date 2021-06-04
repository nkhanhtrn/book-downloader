PS3="Select an option and press Enter: "
options=("Download Manga" "Update Software" "Others" "QUIT")

select opt in "${options[@]}"
do
  case $REPLY in
    1)
      cd ~/Downloads/Manga && python3 parser.py
      ;;
    2)
      cd ~/Downloads/Manga && git pull origin master && python3 -m pip install -r requirements.txt
      ;;
    3)
      break
      ;;
    4)
      kill -9 $PPID
      ;;
    *) echo "invalid option $REPLY";;
  esac
done