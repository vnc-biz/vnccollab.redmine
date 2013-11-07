from setuptools import setup, find_packages
import os

version = '1.0.2'

setup(name='vnccollab.redmine',
      version=version,
      description="VNC Collaboration Redmine AddOn.",
      long_description=open("README.txt").read() + "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
      ],
      keywords='',
      author='Jose Dinuncio',
      author_email='jose.dinuncio@vnc.biz',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['vnccollab'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pyactiveresource',
          'five.grok',
          'plone.api',
          'collective.customizablePersonalizeForm',
          'vnccollab.common'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
