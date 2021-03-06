#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests
from unittestzero import Assert
from pages.desktop.home import HomePage


class TestHomePage:

    @pytest.mark.nondestructive
    def test_major_link_urls_are_valid(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        bad_urls = []
        for link in home_page.major_links_list:
            url = home_page.link_destination(link.get('locator'))
            response_code = home_page.get_response_code(url)
            if response_code != requests.codes.ok:
                bad_urls.append('%s is not a valid url - status code: %s.' % (url, response_code))
        Assert.equal(0, len(bad_urls), '%s bad urls found: ' % len(bad_urls) + ', '.join(bad_urls))

    @pytest.mark.nondestructive
    def test_major_link_destinations_are_correct(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        bad_links = []
        for link in home_page.major_links_list:
            url = home_page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))

    @pytest.mark.nondestructive
    def test_footer_link_destinations_are_correct(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        bad_links = []
        for link in HomePage.Footer.footer_links_list:
            url = home_page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))

    @pytest.mark.nondestructive
    def test_footer_links_are_valid(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        bad_urls = []
        for link in HomePage.Footer.footer_links_list:
            url = home_page.link_destination(link.get('locator'))
            response_code = home_page.get_response_code(url)
            if response_code != requests.codes.ok:
                bad_urls.append('%s is not a valid url - status code: %s.' % (url, response_code))
        Assert.equal(0, len(bad_urls), '%s bad links found: ' % len(bad_urls) + ', '.join(bad_urls))

    @pytest.mark.nondestructive
    def test_images_are_visible(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        bad_images = []
        for image in home_page.images_list:
            if not home_page.is_element_visible(*image.get('locator')):
                bad_images.append('The image at %s is not visible' % image.get('locator')[1:])
        Assert.equal(0, len(bad_images), '%s bad images found: ' % len(bad_images) + ', '.join(bad_images))

    @pytest.mark.nondestructive
    def test_image_srcs_are_correct(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        bad_images = []
        for image in home_page.images_list:
            src = home_page.image_source(image.get('locator'))
            if not src.endswith(image.get('img_name_suffix')):
                bad_images.append('%s does not end with %s' % (src, image.get('img_name_suffix')))
        Assert.equal(0, len(bad_images), '%s bad images found: ' % len(bad_images) + ', '.join(bad_images))

    @pytest.mark.nondestructive
    def test_sign_up_form_is_visible(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        Assert.true(home_page.is_sign_up_form_present, 'The sign up form is not present on the page.')

    @pytest.mark.nondestructive
    def test_sign_up_form_link_destinations_are_correct(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        bad_links = []
        for link in home_page.sign_up_form_link_list:
            url = home_page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        Assert.equal(0, len(bad_links), '%s bad links found: ' % len(bad_links) + ', '.join(bad_links))

    @pytest.mark.nondestructive
    def test_sign_up_form_link_urls_are_valid(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        home_page.go_to_page()
        bad_urls = []
        for link in home_page.sign_up_form_link_list:
            url = home_page.link_destination(link.get('locator'))
            response_code = home_page.get_response_code(url)
            if response_code != requests.codes.ok:
                bad_urls.append('%s is not a valid url - status code: %s.' % (url, response_code))
        Assert.equal(0, len(bad_urls), '%s bad urls found: ' % len(bad_urls) + ', '.join(bad_urls))

    def test_sign_up_form_submit_is_successful(self, mozwebqa):
        home_page = HomePage(mozwebqa)
        valid_email = 'noreply@mozilla.com'
        country = 'US'
        success_url_slug = 'sign-up-for-mozilla'
        home_page.go_to_page()
        home_page.expand_sign_up_form()
        home_page.wait_for_element_visible(*home_page._sign_up_form_privacy_checkbox_locator)
        home_page.input_email(valid_email)
        home_page.select_option(country, home_page._sign_up_form_country_select_locator)
        home_page.check_privacy_checkbox()
        home_page.submit_form()
        Assert.true(success_url_slug in home_page.url_current_page,
                    'Expected current URL slug to be %s, but was not found in %s.' %
                    (success_url_slug, home_page.url_current_page))
