# Usage: 
#
# $ make - builds the contents of src into a deb package using fpm. 
#          control information is stored in ./info
#
# $ make install - installs the last build deb package onto the localhost.
#
# $ make publish - publishes the last build deb package to the site apt repository
#

all:
	./info/bin/build-deb
   
install:
	sudo dpkg -i $(shell ls ./*.deb | sort -r | head -1)

publish:
	./info/bin/publish-deb stable $(shell ls ./*.deb | sort -r | head -1)

clean:
	rm -v *.deb
