.PHONY: all build install test

all:
	@echo "Possible Commands"
	@echo "\tbuild: Builds baseofdata"
	@echo "\tinstall: Installs via pip, needs to be built before installing"
	@echo "\ttest: Starts test server, needs baseofdata to installed via pip"

build:
	@python3 -m build

install:
	@python3 -m pip uninstall baseofdata -y
	@cd dist; python3 -m pip install *.whl

test:
	@cd tests; python3 main.py

clean:
	@rm -rfv dist
	@rm -rfv src/baseofdata.egg-info
	@rm -rfv build