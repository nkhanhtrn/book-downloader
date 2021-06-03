echo "Choose your option: "
echo "  1) Download Manga"
echo "  2) Update Mange Software"
echo "  3) Others"
echo "  4) QUIT"

options=(1 2 3 4)
select opt in "${options[@]}"
do
  case $opt in
    1)
      cd ~/Downloads/Manga && python3 parser.py
      ;;
    2)
      cd ~/Downloads/Manga && git update origin master
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