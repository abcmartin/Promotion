cd "/Users/martin/dissop/context/04_Ergenissse_CD44_Auswertungen_IHC_für_Martin"

prefix="CD44_"

for file in image*.png; do
  if [ -f "$file" ]; then
    mv "$file" "${prefix}${file}"
  fi
done
