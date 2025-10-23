.PHONY: clean clean-test clean-pyc clean-build help install-docx

help:
	@echo "清理命令:"
	@echo "  clean-build - 删除构建制品"
	@echo "  clean-pyc  - 删除Python文件制品"
	@echo "  clean-test - 删除测试和覆盖制品"
	@echo "  clean      - 执行以上所有清理"
	@echo "测试命令:"
	@echo "  test       - 运行测试"
	@echo "  lint       - 检查代码风格"
	@echo "  coverage   - 检查代码覆盖率"
	@echo "构建命令:"
	@echo "  build      - 构建包"
	@echo "  install    - 安装包"
	@echo "依赖命令:"
	@echo "  install-docx - 安装DOCX处理依赖"

clean: clean-build clean-pyc clean-test

clean-build:
	@echo "清理构建制品..."
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +


clean-pyc:
	@echo "清理Python文件制品..."
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


clean-test:
	@echo "清理测试制品..."
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache


test:
	@echo "运行测试..."
	python -m pytest


lint:
	@echo "检查代码风格..."
	flake8 src tests


coverage:
	@echo "检查代码覆盖率..."
	python -m pytest --cov=src tests/


build: clean
	@echo "构建包..."
	python -m build


install: clean
	@echo "安装包..."
	pip install -e .


install-docx:
	@echo "安装DOCX处理依赖..."
	pip install python-docx
