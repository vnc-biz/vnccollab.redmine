from setuptools import setup, find_packages
import os

version = open('version.txt').read()

setup(name='vnccollab.redmine',
      version=version,
      description="VNC Collaboration Redmine AddOn.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Programming Language :: Python",
          "Operating System :: OS Independent",
      ],
      keywords='redmine',
      author='Jose Dinuncio',
      author_email='jose.dinuncio@vnc.biz',
      url='https://github.com/vnc-biz/vnccollab.redmine',
      license='gpl',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['vnccollab'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'textile',
          'pyactiveresource==1.0.1',
          'five.grok',
          'plone.api',
          'plone.app.jquery>=1.7.2',
          'plone.app.jquerytools>=1.4',
          'collective.customizablePersonalizeForm',
          'vnccollab.common'
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
