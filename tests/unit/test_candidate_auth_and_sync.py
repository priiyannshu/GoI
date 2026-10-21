#!/usr/bin/env python3
"""
Unit and Integration Test Suite: Candidate Authentication & Cloudflare DB Propagation
Verifies:
1. 4-digit PIN registration with Candidate Name
2. Generation of unique Candidate ID (e.g. CAN-XXXXXXXX)
3. Same-name candidate isolation with different PINs mapping to unique Candidate IDs
4. Login with Name + 4-digit PIN retrieving specific candidate identity
5. Profile propagation to Cloudflare D1 database
6. Profile retrieval upon login
7. Rejection of invalid PIN format (< 4 or > 4 digits, non-numeric)
"""

import unittest
import json
import urllib.request
import urllib.error
import uuid

WORKER_BASE_URL = "https://grade-a-api.priyanshukh1201.workers.dev"

def make_request(url, method="GET", data=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; GradeAIntelligenceTest/1.0)",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            body = response.read().decode("utf-8")
            return {"status": response.status, "json": json.loads(body) if body else {}}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"raw": body}
        return {"status": e.code, "json": parsed}

class TestCandidateAuthAndSync(unittest.TestCase):

    def test_01_invalid_pin_rejected(self):
        # 3 digits
        payload = json.dumps({"candidate_name": "Test User", "pin": "123"}).encode("utf-8")
        res = make_request(f"{WORKER_BASE_URL}/api/v1/auth/register", method="POST", data=payload)
        self.assertEqual(res["status"], 400)
        self.assertIn("PIN must be exactly 4 numeric digits", res["json"].get("message", ""))

        # 5 digits
        payload = json.dumps({"candidate_name": "Test User", "pin": "12345"}).encode("utf-8")
        res = make_request(f"{WORKER_BASE_URL}/api/v1/auth/register", method="POST", data=payload)
        self.assertEqual(res["status"], 400)

        # Alpha PIN
        payload = json.dumps({"candidate_name": "Test User", "pin": "abcd"}).encode("utf-8")
        res = make_request(f"{WORKER_BASE_URL}/api/v1/auth/register", method="POST", data=payload)
        self.assertEqual(res["status"], 400)

    def test_02_register_candidate_and_receive_unique_id(self):
        cand_name = f"Candidate_{uuid.uuid4().hex[:6]}"
        payload = json.dumps({"candidate_name": cand_name, "pin": "2468"}).encode("utf-8")
        res = make_request(f"{WORKER_BASE_URL}/api/v1/auth/register", method="POST", data=payload)
        self.assertEqual(res["status"], 200)
        self.assertTrue(res["json"].get("success"))
        unique_id = res["json"].get("user_id")
        self.assertTrue(unique_id.startswith("CAN-"))
        self.assertEqual(res["json"].get("candidate_name"), cand_name)

    def test_03_same_candidate_name_different_pins_unique_ids(self):
        shared_name = f"SharedName_{uuid.uuid4().hex[:6]}"

        # Candidate A
        payload_a = json.dumps({"candidate_name": shared_name, "pin": "1111"}).encode("utf-8")
        res_a = make_request(f"{WORKER_BASE_URL}/api/v1/auth/register", method="POST", data=payload_a)
        self.assertEqual(res_a["status"], 200)
        user_id_a = res_a["json"]["user_id"]

        # Candidate B (Identical Name, different PIN)
        payload_b = json.dumps({"candidate_name": shared_name, "pin": "2222"}).encode("utf-8")
        res_b = make_request(f"{WORKER_BASE_URL}/api/v1/auth/register", method="POST", data=payload_b)
        self.assertEqual(res_b["status"], 200)
        user_id_b = res_b["json"]["user_id"]

        # Ensure different unique IDs behind the scenes
        self.assertNotEqual(user_id_a, user_id_b)

        # Login as Candidate A
        login_a = make_request(
            f"{WORKER_BASE_URL}/api/v1/auth/login",
            method="POST",
            data=json.dumps({"candidate_name": shared_name, "pin": "1111"}).encode("utf-8")
        )
        self.assertEqual(login_a["status"], 200)
        self.assertEqual(login_a["json"]["user_id"], user_id_a)

        # Login as Candidate B
        login_b = make_request(
            f"{WORKER_BASE_URL}/api/v1/auth/login",
            method="POST",
            data=json.dumps({"candidate_name": shared_name, "pin": "2222"}).encode("utf-8")
        )
        self.assertEqual(login_b["status"], 200)
        self.assertEqual(login_b["json"]["user_id"], user_id_b)

    def test_04_profile_propagation_to_d1_and_retrieval(self):
        cand_name = f"PropagateCandidate_{uuid.uuid4().hex[:6]}"
        reg_payload = json.dumps({"candidate_name": cand_name, "pin": "7788"}).encode("utf-8")
        reg_res = make_request(f"{WORKER_BASE_URL}/api/v1/auth/register", method="POST", data=reg_payload)
        user_id = reg_res["json"]["user_id"]

        # Propagate profile to Cloudflare D1
        profile_data = {
            "user_id": user_id,
            "name": cand_name,
            "dob": "1998-07-21",
            "gender": "FEMALE",
            "category": "GEN",
            "graduation_degree": "Bachelor",
            "graduation_discipline": "Electronics",
            "graduation_aggregate_pct": 84.5,
            "is_final_year": False,
            "state_domicile": "Tamil Nadu",
            "mother_tongue": "Tamil",
        }
        sync_res = make_request(
            f"{WORKER_BASE_URL}/api/v1/profile/sync",
            method="POST",
            data=json.dumps(profile_data).encode("utf-8")
        )
        self.assertEqual(sync_res["status"], 200)
        self.assertEqual(sync_res["json"]["status"], "synced")
        self.assertTrue(sync_res["json"]["persisted_to_d1"])

        # Login and verify profile is loaded
        login_res = make_request(
            f"{WORKER_BASE_URL}/api/v1/auth/login",
            method="POST",
            data=json.dumps({"candidate_name": cand_name, "pin": "7788"}).encode("utf-8")
        )
        self.assertEqual(login_res["status"], 200)
        loaded_prof = login_res["json"]["profile"]
        self.assertIsNotNone(loaded_prof)
        self.assertEqual(loaded_prof["user_id"], user_id)
        self.assertEqual(loaded_prof["graduation_discipline"], "Electronics")
        self.assertEqual(loaded_prof["state_domicile"], "Tamil Nadu")

if __name__ == "__main__":
    unittest.main()
