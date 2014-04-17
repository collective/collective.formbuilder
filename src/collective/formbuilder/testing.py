# -*- coding: utf-8 -*-
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.formbuilder


FORMBUILDER = PloneWithPackageLayer(
    zcml_package=collective.formbuilder,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.formbuilder:default',
    name="FORMBUILDER")

FORMBUILDER_INTEGRATION = IntegrationTesting(
    bases=(FORMBUILDER, ),
    name="FORMBUILDER_INTEGRATION")

FORMBUILDER_FUNCTIONAL = FunctionalTesting(
    bases=(FORMBUILDER, ),
    name="FORMBUILDER_FUNCTIONAL")
