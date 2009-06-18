#!/usr/bin/env python
# @author Stefano Borini 

from distutils.core import setup

setup(name='Chestnut',
      version='2.2.0',
      author="Stefano Borini",
      author_email="moc.liamg@tuntsehc+inirob.onafets",
      url="http://chestnut.sourceforge.net",
      maintainer="Stefano Borini",
      maintainer_email="moc.liamg@tuntsehc+inirob.onafets",
      description="Programs and module to handle packaged applications",
      packages=['Chestnut'],
      package_dir={'Chestnut' : 'src/Chestnut'},
      scripts=['src/cnrun', 'src/cnpath', 'src/cnls']
      )

