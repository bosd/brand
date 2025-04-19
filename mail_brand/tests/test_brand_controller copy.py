import base64

from odoo.modules import get_resource_path
from odoo.tests import HttpCase


class TestBrandController(HttpCase):
    def test_company_logo_brand(self):
        module_name = "mail_brand"
        icon_path = get_resource_path(module_name, "static", "description", "icon.png")
        with open(icon_path, "rb") as f:
            icon_bytes = f.read()
            icon_base64 = base64.b64encode(icon_bytes)

        brand_partner = self.env["res.partner"].create(
            {"name": "Test Brand Partner", "image_1920": icon_base64}
        )
        brand = self.env["res.brand"].create({"partner_id": brand_partner.id})
        response = self.url_open(f"/logo.png?company={brand.id}&bstyle=1")
        self.assertEqual(response.status_code, 200, "Controller should return success")
        self.assertEqual(
            response.headers["Content-Type"],
            "image/png",
            "Content type should be image/png",
        )

        fetched_brand = self.env["res.brand"].browse(brand.id)
        self.assertTrue(
            response.content == base64.b64decode(fetched_brand.logo_web),
            "Logo content should match computed logo_web",
        )

    def test_company_logo_default(self):
        response = self.url_open("/logo.png?company=1&bstyle=0")
        self.assertEqual(response.status_code, 200, "Controller should return success")
        self.assertEqual(
            response.headers["Content-Type"],
            "image/png",
            "Content type should be image/png",
        )
