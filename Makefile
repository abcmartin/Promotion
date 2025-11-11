.PHONY: html pdf clean

html:
	# TODO: hier Rootstock/Manubot HTML-Build einbinden
	mkdir -p public
	# beispielhafter Output
	echo "<html><body><h1>CD44 Manuskript</h1></body></html>" > public/index.html

pdf:
	mkdir -p output
	# TODO: hier PDF-Build (pandoc/latex/manubot) einbinden
	echo "PDF placeholder for CD44 Manuskript" > output/manuscript.pdf

clean:
	rm -rf public
	rm -rf output
