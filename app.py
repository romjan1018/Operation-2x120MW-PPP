import datetime
import json
import os
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Power Plant Operation System", page_icon="⚡", layout="wide"
)

# -------------------------------------------------------------
# Database File Management (Users & Notices)
# -------------------------------------------------------------
USERS_FILE = "users_db.json"
NOTICES_FILE = "notices_db.json"

default_users = {
    "SHIFT-1ST": {
        "full_name": "Shift In-Charge 1st",
        "designation": "Shift Admin",
        "pin": "1111",
        "role": "Admin",
        "approved": True,
    },
    "SHIFT-2ND": {
        "full_name": "Shift In-Charge 2nd",
        "designation": "Shift Admin",
        "pin": "2222",
        "role": "Admin",
        "approved": True,
    },
    "SHIFT-3RD": {
        "full_name": "Shift In-Charge 3rd",
        "designation": "Shift Admin",
        "pin": "3333",
        "role": "Admin",
        "approved": True,
    },
    "SHIFT-4TH": {
        "full_name": "Shift In-Charge 4th",
        "designation": "Shift Admin",
        "pin": "4444",
        "role": "Admin",
        "approved": True,
    },
}


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for admin_id, admin_info in default_users.items():
                    if admin_id not in data:
                        data[admin_id] = admin_info
                return data
            except:
                return default_users
    return default_users


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def load_notices():
    default_notice_list = [
        "Urgent: Please submit shift handover reports on time."
    ]
    if os.path.exists(NOTICES_FILE):
        with open(NOTICES_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
            except:
                pass
    return default_notice_list


def save_notices(notices):
    with open(NOTICES_FILE, "w", encoding="utf-8") as f:
        json.dump(notices, f, ensure_ascii=False, indent=4)


# -------------------------------------------------------------
# Persistent Session State Setup
# -------------------------------------------------------------
if "users_db" not in st.session_state:
    st.session_state.users_db = load_users()
    save_users(st.session_state.users_db)

if "notices" not in st.session_state:
    st.session_state.notices = load_notices()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "full_name" not in st.session_state:
    st.session_state.full_name = ""
if "designation" not in st.session_state:
    st.session_state.designation = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""

# Navigation session state
if "active_page" not in st.session_state:
    st.session_state.active_page = "🏠 Home Page"

if "selected_shift_view" not in st.session_state:
    st.session_state.selected_shift_view = None

# Shift Members Database
if "shift_members" not in st.session_state:
    st.session_state.shift_members = {
        "Shift 1": [
            "Tarak Das",
            "Hasibur Rahman",
            "Kawsar Khan",
            "Oaliullah",
            "Zahirul Islam",
            "Abdullah Al Kafi",
        ],
        "Shift 2": [
            "Shamim Ahamed",
            "Tarek Rahman",
            "Roman Sarwar",
            "Md. Habibullah",
            "Sabbir Hossain",
            "Robiul Hsan Rony",
            "Muhammad Osman",
        ],
        "Shift 3": [
            "Mohammed Saad Uddin",
            "Md. Romjan Ali",
            "Mejbaul Alam",
            "Atiqur Rahman",
            "Ziaull Haque",
            "Mozammel Hosain",
        ],
        "Shift 4": [
            "Aminul Islam Khan",
            "Debasish Karmaker",
            "Eftakhayrul Haque Emon",
            "Mamun Hossain",
            "Masum Mia",
            "Bourhan Uddin",
        ],
        "OA-1": ["Amir Hossain"],
        "OA-2": ["Sohel Rana"],
    }

# -------------------------------------------------------------
# 1. Login and Sign-Up Panel
# -------------------------------------------------------------
if not st.session_state.logged_in:
    st.title("⚡ Power Plant Operation System")
    st.markdown("### 🔐 Portal Access")

    auth_tab1, auth_tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

    with auth_tab1:
        st.caption("Enter your User ID and Password:")
        with st.form("login_form"):
            raw_user_id = st.text_input("User ID:").strip()
            input_password = st.text_input("Password:", type="password")
            login_btn = st.form_submit_button("Login")

            if login_btn:
                formatted_user_id = raw_user_id.upper()
                user_info = st.session_state.users_db.get(formatted_user_id)

                if not user_info:
                    for uid in list(st.session_state.users_db.keys()):
                        if uid.upper() == formatted_user_id:
                            formatted_user_id = uid
                            user_info = st.session_state.users_db.get(uid)
                            break

                if not user_info:
                    st.error("User ID not found!")
                elif user_info["pin"] != input_password:
                    st.error("Invalid password!")
                elif not user_info.get("approved", False):
                    st.warning("Account pending admin approval.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.user_id = formatted_user_id
                    st.session_state.full_name = user_info.get(
                        "full_name", formatted_user_id
                    )
                    st.session_state.designation = user_info.get(
                        "designation", "Engineer"
                    )
                    st.session_state.user_role = user_info.get(
                        "role", "Engineer"
                    )

                    st.success("Login successful!")
                    st.rerun()

    with auth_tab2:
        st.caption("Fill details for new account (Approval required):")
        with st.form("signup_form"):
            new_fullname = st.text_input("Full Name:").strip()
            new_designation = st.text_input("Designation:").strip()
            new_userid_raw = st.text_input("Preferred User ID:").strip()
            new_password = st.text_input("Password:", type="password")

            signup_btn = st.form_submit_button("Sign Up")

            if signup_btn:
                new_userid = new_userid_raw.upper()
                if (
                    new_fullname
                    and new_designation
                    and new_userid
                    and new_password
                ):
                    if new_userid in st.session_state.users_db:
                        st.error("User ID already taken! Try another.")
                    else:
                        st.session_state.users_db[new_userid] = {
                            "full_name": new_fullname,
                            "designation": new_designation,
                            "pin": new_password,
                            "role": "Engineer",
                            "approved": False,
                        }
                        save_users(st.session_state.users_db)
                        st.success(
                            "Registration sent! Wait for admin approval."
                        )
                else:
                    st.warning("Please fill in all fields.")

else:
    # -------------------------------------------------------------
    # 2. Main Dashboard & Navigation
    # -------------------------------------------------------------
    st.sidebar.title(f"👤 {st.session_state.full_name}")
    st.sidebar.caption(f"📌 {st.session_state.designation}")
    st.sidebar.info(f"Role: {st.session_state.user_role}")
    st.sidebar.markdown("---")

    nav_options = ["🏠 Home Page", "📅 Duty Roster"]
    if st.session_state.user_role == "Admin":
        nav_options.append("🛠️ Admin Control")

    if st.session_state.active_page not in nav_options:
        st.session_state.active_page = "🏠 Home Page"

    selected_page = st.sidebar.radio(
        "Navigation Menu",
        nav_options,
        index=nav_options.index(st.session_state.active_page),
    )
    st.session_state.active_page = selected_page

    st.sidebar.markdown("---")

    # Admin Password Change Option
    if st.session_state.user_role == "Admin":
        with st.sidebar.expander("🔑 Change Password"):
            with st.form("change_pass_form"):
                old_pass = st.text_input("Current Password:", type="password")
                new_pass = st.text_input("New Password:", type="password")
                confirm_pass = st.text_input(
                    "Confirm New Password:", type="password"
                )
                pass_change_btn = st.form_submit_button("Update")

                if pass_change_btn:
                    current_user_data = st.session_state.users_db.get(
                        st.session_state.user_id, {}
                    )
                    if current_user_data.get("pin") != old_pass:
                        st.error("Incorrect current password!")
                    elif not new_pass or (new_pass != confirm_pass):
                        st.error("Passwords do not match!")
                    else:
                        st.session_state.users_db[st.session_state.user_id][
                            "pin"
                        ] = new_pass
                        save_users(st.session_state.users_db)
                        st.success("Password updated!")

        st.sidebar.markdown("---")

    if st.sidebar.button("🔄 Refresh"):
        st.rerun()

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = ""
        st.session_state.full_name = ""
        st.session_state.designation = ""
        st.session_state.user_role = ""
        st.session_state.active_page = "🏠 Home Page"
        st.rerun()

    # =============================================================
    # 🏠 HOME PAGE
    # =============================================================
    if selected_page == "🏠 Home Page":
        col_logo, col_title = st.columns([1, 4])
        with col_logo:
            st.image(
                "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                width=100,
            )
        with col_title:
            st.title("⚡ Power Plant Operation System")
            st.caption(
                "Electricity Generation Company of Bangladesh PLC (EGBPLC)"
            )

        st.markdown("---")

        st.markdown("### 🚀 Quick Navigation")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📅 Go to Duty Roster", use_container_width=True):
                st.session_state.active_page = "📅 Duty Roster"
                st.rerun()
        with c2:
            st.button(
                "📊 Energy Monitoring (Coming Soon)",
                use_container_width=True,
                disabled=True,
            )
        with c3:
            st.button(
                "📋 Reports & Handover (Coming Soon)",
                use_container_width=True,
                disabled=True,
            )

        st.markdown("---")

        st.markdown("### 📢 Temporary Notice Board")

        # Notice Publishing Section (Direct text input and button outside strict forms)
        notice_input = st.text_input(
            "Write a new notice:", key="notice_input_field"
        )
        if st.button("Publish Notice"):
            if notice_input.strip():
                # Load latest from file first to avoid overwriting conflicts
                current_list = load_notices()
                current_list.append(
                    f"{notice_input.strip()} (By: {st.session_state.full_name})"
                )
                save_notices(current_list)
                st.session_state.notices = current_list
                st.success("Notice published successfully!")
                st.rerun()
            else:
                st.warning("Please write something for the notice.")

        st.markdown("#### Active Notices:")
        # Always fetch latest from file
        active_notices = load_notices()
        st.session_state.notices = active_notices

        if not active_notices or len(active_notices) == 0:
            st.info("No active notices.")
        else:
            for idx, notice in enumerate(active_notices):
                col_n1, col_n2 = st.columns([8, 2])
                with col_n1:
                    st.markdown(f"📌 {notice}")
                with col_n2:
                    if st.session_state.user_role == "Admin" or st.button(
                        "Delete", key=f"del_notice_{idx}"
                    ):
                        active_notices.pop(idx)
                        save_notices(active_notices)
                        st.session_state.notices = active_notices
                        st.success("Notice deleted!")
                        st.rerun()

    # =============================================================
    # 📅 DUTY ROSTER PAGE
    # =============================================================
    elif selected_page == "📅 Duty Roster":
        if st.button("🏠 Back to Home Page"):
            st.session_state.active_page = "🏠 Home Page"
            st.rerun()

        st.markdown("### 🔍 Search Shift Duty")
        selected_search_date = st.date_input(
            "Select Date:", datetime.date.today()
        )

        shift_pattern = [
            {"1": "0", "2": "A", "3": "C", "4": "B"},
            {"1": "0", "2": "A", "3": "C", "4": "B"},
            {"1": "B", "2": "C", "3": "0", "4": "A"},
            {"1": "B", "2": "C", "3": "0", "4": "A"},
            {"1": "A", "2": "0", "3": "B", "4": "C"},
            {"1": "A", "2": "0", "3": "B", "4": "C"},
            {"1": "C", "2": "B", "3": "A", "4": "0"},
            {"1": "C", "2": "B", "3": "A", "4": "0"},
        ]

        oa_pattern = [
            {"OA1": "G", "OA2": "0"},
            {"OA1": "A", "OA2": "B"},
            {"OA1": "A", "OA2": "B"},
            {"OA1": "0", "OA2": "G"},
            {"OA1": "B", "OA2": "A"},
            {"OA1": "B", "OA2": "A"},
        ]

        base_date = datetime.date(2026, 10, 28)
        search_day_diff = (selected_search_date - base_date).days

        s_pat = shift_pattern[search_day_diff % 8]
        o_pat = oa_pattern[search_day_diff % 6]

        st.success(
            f"📅 Status for {selected_search_date.strftime('%d-%b-%Y (%A)')}:"
        )

        st.markdown(
            "👇 *শIFT বা OA-এর ওপর ক্লিক করে মেম্বারদের তালিকা দেখুন:*"
        )
        b1, b2, b3, b4, b5, b6 = st.columns(6)

        with b1:
            if st.button("Shift 1", use_container_width=True):
                st.session_state.selected_shift_view = "Shift 1"
        with b2:
            if st.button("Shift 2", use_container_width=True):
                st.session_state.selected_shift_view = "Shift 2"
        with b3:
            if st.button("Shift 3", use_container_width=True):
                st.session_state.selected_shift_view = "Shift 3"
        with b4:
            if st.button("Shift 4", use_container_width=True):
                st.session_state.selected_shift_view = "Shift 4"
        with b5:
            if st.button("OA-1", use_container_width=True):
                st.session_state.selected_shift_view = "OA-1"
        with b6:
            if st.button("OA-2", use_container_width=True):
                st.session_state.selected_shift_view = "OA-2"

        if st.session_state.selected_shift_view:
            sh_name = st.session_state.selected_shift_view
            members = st.session_state.shift_members.get(sh_name, [])
            members_str = ", ".join(members)
            st.info(f"👥 *{sh_name} Members:* {members_str}")

        single_row_html = f"""
        <div style="overflow-x: auto; width: 100%; margin-top: 10px; margin-bottom: 20px;">
            <table style="width: 100%; border-collapse: collapse; border: 2px solid black; background-color: white; text-align: center; font-family: sans-serif;">
                <tr style="background-color: #262626; color: white; font-size: 13px;">
                    <th style="border: 1px solid black; padding: 6px;">Shift 1</th>
                    <th style="border: 1px solid black; padding: 6px;">Shift 2</th>
                    <th style="border: 1px solid black; padding: 6px;">Shift 3</th>
                    <th style="border: 1px solid black; padding: 6px;">Shift 4</th>
                    <th style="border: 1px solid black; padding: 6px;">OA-1</th>
                    <th style="border: 1px solid black; padding: 6px;">OA-2</th>
                </tr>
                <tr style="font-weight: bold; font-size: 16px; color: #000000;">
                    <td style="border: 1px solid black; padding: 10px;">{s_pat["1"]}</td>
                    <td style="border: 1px solid black; padding: 10px;">{s_pat["2"]}</td>
                    <td style="border: 1px solid black; padding: 10px;">{s_pat["3"]}</td>
                    <td style="border: 1px solid black; padding: 10px;">{s_pat["4"]}</td>
                    <td style="border: 1px solid black; padding: 10px;">{o_pat["OA1"]}</td>
                    <td style="border: 1px solid black; padding: 10px;">{o_pat["OA2"]}</td>
                </tr>
            </table>
        </div>
        """
        st.markdown(single_row_html, unsafe_allow_html=True)

        st.markdown("---")

        today = datetime.date.today()
        current_year = today.strftime("%Y")

        html_table = (
            '<div style="width: 100%; max-width: 900px; max-height: 500px; overflow-y: auto; overflow-x: auto; margin: 0 auto; font-family: sans-serif; border: 2px solid black;">'
            '<table style="width: 100%; border-collapse: collapse; background-color: white;">'
            "<thead>"
            '<tr>'
            '<th colspan="8" style="position: sticky; top: 0; z-index: 4; background-color: #7b113a; color: white; padding: 12px; text-align: center; border-bottom: 2px solid black; font-size: 22px; letter-spacing: 2px;">DUTY ROSTER</th>'
            "</tr>"
            '<tr>'
            f'<th colspan="8" style="position: sticky; top: 51px; z-index: 3; background-color: #ffffff; color: #cc0000; padding: 6px; text-align: center; border-bottom: 2px solid black; font-size: 18px; font-weight: bold;">{current_year}</th>'
            "</tr>"
            '<tr style="background-color: #262626; color: white;">'
            '<th style="position: sticky; top: 95px; z-index: 2; border: 1px solid black; padding: 8px; text-align: center; font-size: 15px; background-color: #262626;">Date</th>'
            '<th style="position: sticky; top: 95px; z-index: 2; border: 1px solid black; padding: 8px; text-align: center; font-size: 15px; background-color: #262626;">Day</th>'
            '<th style="position: sticky; top: 95px; z-index: 2; border: 1px solid black; padding: 8px; text-align: center; font-size: 15px; background-color: #262626;">Shift 1</th>'
            '<th style="position: sticky; top: 95px; z-index: 2; border: 1px solid black; padding: 8px; text-align: center; font-size: 15px; background-color: #262626;">Shift 2</th>'
            '<th style="position: sticky; top: 95px; z-index: 2; border: 1px solid black; padding: 8px; text-align: center; font-size: 15px; background-color: #262626;">Shift 3</th>'
            '<th style="position: sticky; top: 95px; z-index: 2; border: 1px solid black; padding: 8px; text-align: center; font-size: 15px; background-color: #262626;">Shift 4</th>'
            '<th style="position: sticky; top: 95px; z-index: 2; border: 1px solid black; padding: 8px; text-align: center; font-size: 15px; background-color: #262626;">OA-1</th>'
            '<th style="position: sticky; top: 95px; z-index: 2; border: 1px solid black; padding: 8px; text-align: center; font-size: 15px; background-color: #262626;">OA-2</th>'
            "</tr>"
            "</thead>"
            "<tbody>"
        )

        for i in range(-8, 26):
            d = today + datetime.timedelta(days=i)
            day_diff = (d - base_date).days

            s_p = shift_pattern[day_diff % 8]
            o_p = oa_pattern[day_diff % 6]

            is_today = d == today
            bg_color = "#ffcccc" if is_today else "#ffffff"
            text_color = "#990000" if is_today else "#000000"
            font_weight = "bold" if is_today else "bold"

            html_table += (
                f'<tr style="background-color: {bg_color}; color: {text_color}; font-weight: {font_weight}; text-align: center;">'
                f'<td style="border: 1px solid black; padding: 8px; font-size: 14px;">{d.strftime("%d-%b")}</td>'
                f'<td style="border: 1px solid black; padding: 8px; font-size: 14px;">{d.strftime("%A")}</td>'
                f'<td style="border: 1px solid black; padding: 8px; font-size: 14px;">{s_p["1"]}</td>'
                f'<td style="border: 1px solid black; padding: 8px; font-size: 14px;">{s_p["2"]}</td>'
                f'<td style="border: 1px solid black; padding: 8px; font-size: 14px;">{s_p["3"]}</td>'
                f'<td style="border: 1px solid black; padding: 8px; font-size: 14px;">{s_p["4"]}</td>'
                f'<td style="border: 1px solid black; padding: 8px; font-size: 14px;">{o_p["OA1"]}</td>'
                f'<td style="border: 1px solid black; padding: 8px; font-size: 14px;">{o_p["OA2"]}</td>'
                "</tr>"
            )

        html_table += "</tbody></table></div>"
        st.markdown(html_table, unsafe_allow_html=True)

    # =============================================================
    # 🛠️ ADMIN CONTROL PAGE
    # =============================================================
    elif selected_page == "🛠️ Admin Control":
        if st.button("🏠 Back to Home Page"):
            st.session_state.active_page = "🏠 Home Page"
            st.rerun()

        st.header("🛠️ Admin Panel")
        st.info(f"Welcome Admin [{st.session_state.full_name}]!")

        tab1, tab2, tab3 = st.tabs(
            [
                "👥 Edit Shift Members",
                "⏳ User Approvals",
                "🔑 Reset User Password",
            ]
        )

        with tab1:
            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown("### ✏️ Transfer Member")
                selected_shift_from = st.selectbox(
                    "Current Shift:",
                    [
                        "Shift 1",
                        "Shift 2",
                        "Shift 3",
                        "Shift 4",
                        "OA-1",
                        "OA-2",
                    ],
                )
                member_list = st.session_state.shift_members[
                    selected_shift_from
                ]

                if member_list:
                    selected_member = st.selectbox(
                        "Select Member:", member_list
                    )
                    selected_shift_to = st.selectbox(
                        "Transfer To:",
                        [
                            "Shift 1",
                            "Shift 2",
                            "Shift 3",
                            "Shift 4",
                            "OA-1",
                            "OA-2",
                        ],
                    )

                    if st.button("Update Shift"):
                        if selected_shift_from != selected_shift_to:
                            st.session_state.shift_members[
                                selected_shift_from
                            ].remove(selected_member)
                            st.session_state.shift_members[
                                selected_shift_to
                            ].append(selected_member)
                            st.success(
                                f"{selected_member} moved to {selected_shift_to}!"
                            )
                            st.rerun()
                        else:
                            st.warning("Select a different shift.")
                else:
                    st.warning("No members in this shift.")

            with col_right:
                st.markdown("### 📝 Edit Shift List")
                target_shift = st.selectbox(
                    "Select Shift:",
                    [
                        "Shift 1",
                        "Shift 2",
                        "Shift 3",
                        "Shift 4",
                        "OA-1",
                        "OA-2",
                    ],
                    key="t_shift",
                )
                current_members = st.session_state.shift_members[target_shift]

                _edited_members_str = st.text_area(
                    "Member Names (One per line):",
                    value="\n".join(current_members),
                )

                if st.button("Save Members"):
                    new_list = [
                        name.strip()
                        for name in _edited_members_str.split("\n")
                        if name.strip()
                    ]
                    st.session_state.shift_members[target_shift] = new_list
                    st.success(f"{target_shift} member list updated!")
                    st.rerun()

        with tab2:
            st.markdown("### ⏳ Pending Approvals")
            pending_users = {
                uid: info
                for uid, info in st.session_state.users_db.items()
                if not info.get("approved", False)
            }

            if not pending_users:
                st.info("No pending users.")
            else:
                for p_uid, p_info in pending_users.items():
                    col_u1, col_u2, col_u3 = st.columns([4, 2, 2])
                    with col_u1:
                        st.markdown(
                            f"👤 *{p_info.get('full_name')}* ({p_info.get('designation')})\n"
                            f"ID: {p_uid}"
                        )
                    with col_u2:
                        if st.button("Approve", key=f"app_{p_uid}"):
                            st.session_state.users_db[p_uid]["approved"] = True
                            save_users(st.session_state.users_db)
                            st.success(
                                f"{p_info.get('full_name')} approved!"
                            )
                            st.rerun()
                    with col_u3:
                        if st.button("Reject", key=f"del_u_{p_uid}"):
                            del st.session_state.users_db[p_uid]
                            save_users(st.session_state.users_db)
                            st.warning(
                                f"{p_info.get('full_name')} rejected."
                            )
                            st.rerun()

        with tab3:
            st.markdown("### 🔑 Reset User Password")
            st.caption("Reset password for engineers who forgot their pin:")
            approved_users_list = [
                uid
                for uid, info in st.session_state.users_db.items()
                if info.get("role") != "Admin" and info.get("approved", True)
            ]

            if approved_users_list:
                with st.form("reset_user_pass_form"):
                    target_user_id = st.selectbox(
                        "Select User ID:", approved_users_list
                    )
                    temp_pass = st.text_input(
                        "New Temporary Password:", type="password"
                    )
                    reset_btn = st.form_submit_button("Reset Password")

                    if reset_btn:
                        if temp_pass:
                            st.session_state.users_db[target_user_id][
                                "pin"
                            ] = temp_pass
                            save_users(st.session_state.users_db)
                            st.success(
                                f"Password reset successfully for {target_user_id}!"
                            )
                        else:
                            st.warning("Enter a valid new password.")
            else:
                st.info("No registered engineers available.")