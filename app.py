import datetime
import json
import os
import pandas as pd
import streamlit as st

# পেজ কনফিগারেশন
st.set_page_config(
    page_title="Power Plant Operation System", page_icon="⚡", layout="wide"
)

# -------------------------------------------------------------
# ইউজার ডাটাবেজ ফাইল ম্যানেজমেন্ট (JSON সেভ করার ব্যবস্থা)
# -------------------------------------------------------------
USERS_FILE = "users_db.json"

# ডিফল্ট ৪ জন নির্দিষ্ট এডমিন (এদের অ্যাকাউন্ট অলরেডি Approved থাকবে)
default_users = {
    "shift1st": {
        "full_name": "Shift In-Charge 1st",
        "designation": "Shift Admin",
        "pin": "1111",
        "role": "Admin",
        "approved": True,
    },
    "shift2nd": {
        "full_name": "Shift In-Charge 2nd",
        "designation": "Shift Admin",
        "pin": "2222",
        "role": "Admin",
        "approved": True,
    },
    "shift3rd": {
        "full_name": "Shift In-Charge 3rd",
        "designation": "Shift Admin",
        "pin": "3333",
        "role": "Admin",
        "approved": True,
    },
    "shift4th": {
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
                return json.load(f)
            except:
                return default_users
    return default_users


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


if "users_db" not in st.session_state:
    st.session_state.users_db = load_users()

# -------------------------------------------------------------
# সেশন স্টেট (লগইন ধরে রাখার জন্য)
# -------------------------------------------------------------
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

# শিফট মেম্বারস এবং OA মেম্বার ডাটাবেজ
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

if "notices" not in st.session_state:
    st.session_state.notices = [
        "জরুরি নোটিশ: শিফট পরিবর্তনের সময় হ্যান্ডওভার রিপোর্ট সঠিকভাবে জমা দিন।"
    ]

# -------------------------------------------------------------
# ১. লগইন এবং সাইন-আপ প্যানেল
# -------------------------------------------------------------
if not st.session_state.logged_in:
    st.title("⚡ Power Plant Operation & Automation System")
    st.markdown("### 🔐 পোর্টাল অ্যাক্সেস প্যানেল")

    auth_tab1, auth_tab2 = st.tabs(["🔑 লগইন (Login)", "📝 সাইন আপ (Sign Up)"])

    # --- লগইন ট্যাব ---
    with auth_tab1:
        st.write("আপনার ইউজার আইডি ও পাসওয়ার্ড দিয়ে প্রবেশ করুন:")
        with st.form("login_form"):
            input_user_id = st.text_input("User ID (ইউজার আইডি):").strip()
            input_password = st.text_input(
                "Password (পাসওয়ার্ড):", type="password"
            )
            login_btn = st.form_submit_button("লগইন করুন")

            if login_btn:
                user_info = st.session_state.users_db.get(input_user_id)

                if not user_info:
                    st.error("এই ইউজার আইডিটি সিস্টেমে পাওয়া যায়নি!")
                elif user_info["pin"] != input_password:
                    st.error("ভুল পাসওয়ার্ড! দয়া করে সঠিক পাসওয়ার্ড দিন।")
                elif not user_info.get("approved", False):
                    st.warning(
                        "আপনার অ্যাকাউন্টটি এখনও এডমিন দ্বারা অনুমোদিত হয়নি। অনুমোদনের জন্য অপেক্ষা করুন।"
                    )
                else:
                    # সফল লগইন এবং সেশন স্টেট সেভ
                    st.session_state.logged_in = True
                    st.session_state.user_id = input_user_id
                    st.session_state.full_name = user_info.get(
                        "full_name", input_user_id
                    )
                    st.session_state.designation = user_info.get(
                        "designation", "Engineer"
                    )
                    st.session_state.user_role = user_info.get(
                        "role", "Engineer"
                    )

                    st.success("লগইন সফল হয়েছে! ড্যাশবোর্ডে প্রবেশ করা হচ্ছে...")
                    st.rerun()

    # --- সাইন আপ ট্যাব ---
    with auth_tab2:
        st.write(
            "নতুন অ্যাকাউন্ট তৈরির জন্য নিচের ঘরগুলো পূরণ করুন (এডমিনের অনুমোদনের পর লগইন করতে পারবেন):"
        )
        with st.form("signup_form"):
            new_fullname = st.text_input("Full Name (পুরো নাম):").strip()
            new_designation = st.text_input(
                "Designation (পদবী/পজিশন):"
            ).strip()
            new_userid = st.text_input(
                "User ID (পছন্দমতো ইউজার আইডি):"
            ).strip()
            new_password = st.text_input(
                "Password (গোপন পাসওয়ার্ড):", type="password"
            )

            signup_btn = st.form_submit_button("সাইন আপ করুন")

            if signup_btn:
                if (
                    new_fullname
                    and new_designation
                    and new_userid
                    and new_password
                ):
                    if new_userid in st.session_state.users_db:
                        st.error(
                            "এই User ID টি ইতিমধ্যে ব্যবহৃত হচ্ছে। অন্য আইডি ব্যবহার করুন।"
                        )
                    else:
                        # নতুন ইউজারের ডাটা সেভ (Approved = False)
                        st.session_state.users_db[new_userid] = {
                            "full_name": new_fullname,
                            "designation": new_designation,
                            "pin": new_password,
                            "role": "Engineer",
                            "approved": False,
                        }
                        save_users(st.session_state.users_db)
                        st.success(
                            f"ধন্যবাদ {new_fullname}! আপনার সাইন-আপ আবেদন জমা হয়েছে। এডমিন অনুমোদন দিলে আপনি এই User ID ও Password দিয়ে লগইন করতে পারবেন।"
                        )
                else:
                    st.warning("দয়া করে প্রতিটি ঘর (Field) সঠিকভাবে পূরণ করুন।")

else:
    # -------------------------------------------------------------
    # ২. মেইন ড্যাশবোর্ড (লগইন থাকা অবস্থায়)
    # -------------------------------------------------------------
    st.sidebar.title(f"👤 {st.session_state.full_name}")
    st.sidebar.caption(f"📌 {st.session_state.designation}")
    st.sidebar.info(f"রোল (Role): {st.session_state.user_role}")
    st.sidebar.markdown("---")

    menu_options = ["ডিউটি রোস্টার ও সার্চ", "টেম্পোরারি নোটিশ বোর্ড"]

    if st.session_state.user_role == "Admin":
        menu_options.append("এডমিন কন্ট্রোল (Shift & User Management)")

    menu = st.sidebar.selectbox("মেনু নির্বাচন করুন", menu_options)

    # -------------------------------------------------------------
    # ৩. পাশের প্যানেলে Shift Members Table প্রদর্শন
    # -------------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👥 Shift Members Table")
    df_side_members = pd.DataFrame(
        {
            "Shift 1": pd.Series(st.session_state.shift_members["Shift 1"]),
            "Shift 2": pd.Series(st.session_state.shift_members["Shift 2"]),
            "Shift 3": pd.Series(st.session_state.shift_members["Shift 3"]),
            "Shift 4": pd.Series(st.session_state.shift_members["Shift 4"]),
            "OA-1": pd.Series(st.session_state.shift_members["OA-1"]),
            "OA-2": pd.Series(st.session_state.shift_members["OA-2"]),
        }
    )
    st.sidebar.dataframe(df_side_members, height=300)

    st.sidebar.markdown("---")

    # --- এডমিনদের জন্য পাসওয়ার্ড পরিবর্তন করার অপশন (Sidebar-এ) ---
    if st.session_state.user_role == "Admin":
        with st.sidebar.expander("🔑 পাসওয়ার্ড পরিবর্তন করুন"):
            with st.form("change_pass_form"):
                old_pass = st.text_input(
                    "বর্তমান পাসওয়ার্ড:", type="password"
                )
                new_pass = st.text_input("নতুন পাসওয়ার্ড:", type="password")
                confirm_pass = st.text_input(
                    "নতুন পাসওয়ার্ড কনফার্ম করুন:", type="password"
                )
                pass_change_btn = st.form_submit_button("পাসওয়ার্ড আপডেট করুন")

                if pass_change_btn:
                    current_user_data = st.session_state.users_db.get(
                        st.session_state.user_id, {}
                    )
                    if current_user_data.get("pin") != old_pass:
                        st.error("বর্তমান পাসওয়ার্ড ভুল হয়েছে!")
                    elif not new_pass or (new_pass != confirm_pass):
                        st.error(
                            "নতুন পাসওয়ার্ড এবং কনফার্ম পাসওয়ার্ড মেলেনি বা খালি রয়েছে!"
                        )
                    else:
                        # পাসওয়ার্ড আপডেট করা
                        st.session_state.users_db[st.session_state.user_id][
                            "pin"
                        ] = new_pass
                        save_users(st.session_state.users_db)
                        st.success(
                            "আপনার পাসওয়ার্ড সফলভাবে পরিবর্তন করা হয়েছে!"
                        )

        st.sidebar.markdown("---")

    # অ্যাপের ভেতরের রিফ্রেশ বাটন
    if st.sidebar.button("🔄 পেজ রিফ্রেশ করুন (Refresh)"):
        st.rerun()

    # ম্যানুয়াল লগআউট বাটন
    if st.sidebar.button("🚪 লগআউট (Logout)"):
        st.session_state.logged_in = False
        st.session_state.user_id = ""
        st.session_state.full_name = ""
        st.session_state.designation = ""
        st.session_state.user_role = ""
        st.rerun()

    # --- মডিউল ক: অটো-আপডেটিং ডায়নামিক রোস্টার ও ডেট সার্চ ---
    if menu == "ডিউটি রোস্টার ও সার্চ":
        st.markdown("### 🔍 নির্দিষ্ট তারিখের ডিউটি সার্চ করুন")
        selected_search_date = st.date_input(
            "তারিখ সিলেক্ট করুন:", datetime.date.today()
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
            f"📅 {selected_search_date.strftime('%d-%b-%Y (%A)')} এর ডিউটি স্ট্যাটাস:"
        )

        single_row_html = f"""
        <div style="overflow-x: auto; width: 100%; margin-bottom: 20px;">
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

        # মূল ডিউটি রোস্টার টেবিল (৯ নং সারিতে আজকের দিন, ওপরে ৮ দিন, নিচে ২৫ দিন)
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

    # --- মডিউল খ: টেম্পোরারি নোটিশ বোর্ড ---
    elif menu == "টেম্পোরারি নোটিশ বোর্ড":
        st.header("📢 টেম্পোরারি নোটিশ বোর্ড")

        with st.form("notice_form"):
            new_notice = st.text_input("নতুন জরুরি নোটিশ লিখুন:")
            add_btn = st.form_submit_button("নোটিশ পোস্ট করুন")
            if add_btn and new_notice:
                st.session_state.notices.append(
                    f"{new_notice} (পোস্ট করেছেন: {st.session_state.full_name})"
                )
                st.success("নোটিশ সফলভাবে যোগ করা হয়েছে!")
                st.rerun()

        st.markdown("### বর্তমান নোটিশসমূহ:")
        if len(st.session_state.notices) == 0:
            st.info("বর্তমানে কোনো নোটিশ নেই।")
        else:
            for idx, notice in enumerate(st.session_state.notices):
                col1, col2 = st.columns([8, 2])
                with col1:
                    st.markdown(f"📌 {notice}")
                with col2:
                    if st.button("ডিলিট / ভ্যানিশ", key=f"del_{idx}"):
                        st.session_state.notices.pop(idx)
                        st.rerun()

    # --- মডিউল গ: এডমিন কন্ট্রোল ---
    elif menu == "এডমিন কন্ট্রোল (Shift & User Management)":
        st.header("🛠️ এডমিন প্যানেল")
        st.info(
            f"স্বাগতম এডমিন [{st.session_state.full_name}]! এখান থেকে শিফট মেম্বার এবং নতুন অ্যাকাউন্ট অনুমোদন করতে পারবেন।"
        )

        tab1, tab2 = st.tabs(
            ["👥 শিফট মেম্বার এডিট", "⏳ ইউজার অনুমোদন (User Approvals)"]
        )

        with tab1:
            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown("### ✏️ মেম্বারের শিফট পরিবর্তন করুন")
                selected_shift_from = st.selectbox(
                    "বর্তমান শিফট সিলেক্ট করুন:",
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
                        "মেম্বারের নাম সিলেক্ট করুন:", member_list
                    )
                    selected_shift_to = st.selectbox(
                        "নতুন কোন শিফটে নিতে চান?",
                        [
                            "Shift 1",
                            "Shift 2",
                            "Shift 3",
                            "Shift 4",
                            "OA-1",
                            "OA-2",
                        ],
                    )

                    if st.button("মেম্বারের শিফট আপডেট করুন"):
                        if selected_shift_from != selected_shift_to:
                            st.session_state.shift_members[
                                selected_shift_from
                            ].remove(selected_member)
                            st.session_state.shift_members[
                                selected_shift_to
                            ].append(selected_member)
                            st.success(
                                f"সফলভাবে {selected_member}-কে {selected_shift_from} থেকে {selected_shift_to}-এ ট্রান্সফার করা হয়েছে!"
                            )
                            st.rerun()
                        else:
                            st.warning(
                                "দয়া করে দুটি আলাদা ক্যাটাগরি সিলেক্ট করুন।"
                            )
                else:
                    st.warning("এই শিফটে বর্তমানে কোনো সদস্য নেই।")

            with col_right:
                st.markdown("### 📝 সরাসরি সদস্যের নাম সংশোধন/এডিট")
                target_shift = st.selectbox(
                    "শিফট নির্বাচন:",
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
                    "সদস্যদের নাম (প্রতি লাইনে একটি নাম লিখুন):",
                    value="\n".join(current_members),
                )

                if st.button("তালিকা সেভ করুন"):
                    new_list = [
                        name.strip()
                        for name in _edited_members_str.split("\n")
                        if name.strip()
                    ]
                    st.session_state.shift_members[target_shift] = new_list
                    st.success(f"{target_shift}-এর মেম্বার লিস্ট আপডেট হয়েছে!")
                    st.rerun()

        with tab2:
            st.markdown(
                "### ⏳ অপেক্ষমাণ ইউজার তালিকা (Pending Approvals)"
            )
            pending_users = {
                uid: info
                for uid, info in st.session_state.users_db.items()
                if not info.get("approved", False)
            }

            if not pending_users:
                st.info("বর্তমানে অনুমোদনের অপেক্ষায় কোনো নতুন ইউজার নেই।")
            else:
                for p_uid, p_info in pending_users.items():
                    col_u1, col_u2, col_u3 = st.columns([4, 2, 2])
                    with col_u1:
                        st.markdown(
                            f"👤 *{p_info.get('full_name')}* ({p_info.get('designation')})\n"
                            f"ID: {p_uid}"
                        )
                    with col_u2:
                        if st.button("অনুমোদন দিন (Approve)", key=f"app_{p_uid}"):
                            st.session_state.users_db[p_uid]["approved"] = True
                            save_users(st.session_state.users_db)
                            st.success(
                                f"{p_info.get('full_name')}-এর অ্যাকাউন্ট অনুমোদিত হয়েছে!"
                            )
                            st.rerun()
                    with col_u3:
                        if st.button(
                            "বাতিল / ডিলিট", key=f"del_u_{p_uid}"
                        ):
                            del st.session_state.users_db[p_uid]
                            save_users(st.session_state.users_db)
                            st.warning(
                                f"{p_info.get('full_name')}-এর আবেদন বাতিল করা হয়েছে।"
                            )
                            st.rerun()