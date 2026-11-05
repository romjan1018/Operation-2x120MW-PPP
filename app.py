import datetime
import pandas as pd
import streamlit as st

# পেজ কনফিগারেশন
st.set_page_config(
    page_title="Power Plant Operation System", page_icon="⚡", layout="wide"
)

# সেশন স্টেট ইনিশিয়ালাইজেশন
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
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

# ইউজার এবং পিন ডাটাবেজ
users_db = {
    "Md. Romjan Ali": {"pin": "1234", "role": "Admin"},
    "Shift In-charge (A)": {"pin": "1111", "role": "Admin"},
    "Shift Engineer - B": {"pin": "2222", "role": "Engineer"},
    "Tarak Das": {"pin": "3333", "role": "Engineer"},
    "Shamim Ahamed": {"pin": "4444", "role": "Engineer"},
}

# -------------------------------------------------------------
# ১. পিন-বেসড সিকিউর লগইন সিস্টেম
# -------------------------------------------------------------
if not st.session_state.logged_in:
    st.title("⚡ Power Plant Operation & Automation System")
    st.markdown("### সিকিউরড লগইন প্যানেল")
    st.write(
        "দয়া করে আপনার নাম সিলেক্ট করুন এবং ৪-ডিজিটের গোপন পিন কোড দিয়ে প্রবেশ করুন।"
    )

    with st.form("login_form"):
        selected_user = st.selectbox(
            "আপনার নাম / আইডি সিলেক্ট করুন:", list(users_db.keys())
        )
        entered_pin = st.text_input(
            "গোপন পিন কোড (4-digit PIN)", type="password"
        )
        submit_btn = st.form_submit_button("লগইন করুন")

        if submit_btn:
            user_info = users_db.get(selected_user)
            if user_info and user_info["pin"] == entered_pin:
                st.session_state.logged_in = True
                st.session_state.user_name = selected_user
                st.session_state.user_role = user_info["role"]
                st.success("লগইন সফল হয়েছে! ড্যাশবোর্ডে প্রবেশ করা হচ্ছে...")
                st.rerun()
            else:
                st.error("ভুল পিন কোড! দয়া করে সঠিক পিন দিয়ে আবার চেষ্টা করুন।")

else:
    # -------------------------------------------------------------
    # ২. মেইন ড্যাশবোর্ড (লগইন হওয়ার পর)
    # -------------------------------------------------------------
    st.sidebar.title(f"👤 {st.session_state.user_name}")
    st.sidebar.info(f"রোল (Role): {st.session_state.user_role}")
    st.sidebar.markdown("---")

    menu_options = ["ডিউটি রোস্টার ও সার্চ", "টেম্পোরারি নোটিশ বোর্ড"]
    if st.session_state.user_role == "Admin":
        menu_options.append("এডমিন কন্ট্রোল (Shift & Member Edit)")

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
    st.sidebar.dataframe(df_side_members, height=320)

    st.sidebar.markdown("---")
    if st.sidebar.button("লগআউট (Logout)"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.user_role = ""
        st.rerun()

    # --- মডিউল ক: অটো-আপডেটিং ডায়নামিক রোস্টার ও ডেট সার্চ ---
    if menu == "ডিউটি রোস্টার ও সার্চ":
        st.markdown("### 🔍 নির্দিষ্ট তারিখের ডিউটি সার্চ করুন")
        selected_search_date = st.date_input(
            "তারিখ সিলেক্ট করুন:", datetime.date.today()
        )

        # মূল শিফট প্যাটার্ন (৮ দিনের সাইকেল)
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

        # OA-1 এবং OA-2 প্যাটার্ন (৬ দিনের সাইকেল)
        oa_pattern = [
            {"OA1": "G", "OA2": "0"},
            {"OA1": "A", "OA2": "B"},
            {"OA1": "A", "OA2": "B"},
            {"OA1": "B", "OA2": "A"},
            {"OA1": "B", "OA2": "A"},
            {"OA1": "G", "OA2": "0"},
        ]

        base_date = datetime.date(2026, 10, 28)
        search_day_diff = (selected_search_date - base_date).days

        s_pat = shift_pattern[search_day_diff % 8]
        o_pat = oa_pattern[search_day_diff % 6]

        st.success(
            f"📅 {selected_search_date.strftime('%d-%b-%Y (%A)')} এর ডিউটি স্ট্যাটাস:"
        )

        # মোবাইলে এক সারিতে দেখানোর জন্য রেসপনসিভ ফ্লেক্সবক্স টেবিল
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
        current_year = datetime.date.today().strftime("%Y")

        # মূল ডিউটি রোস্টার টেবিল (হেডার টেবিলের সাথে সংযুক্ত করা হয়েছে যাতে প্রশস্ততার অমিল না হয়)
        html_table = (
            '<div style="width: 100%; max-width: 900px; margin: 0 auto; font-family: sans-serif; overflow-x: auto;">'
            '<table style="width: 100%; border-collapse: collapse; border: 2px solid black; background-color: white;">'
            "<thead>"
            # DUTY ROSTER Header Row
            '<tr>'
            '<th colspan="8" style="background-color: #7b113a; color: white; padding: 12px; text-align: center; border: 2px solid black; font-size: 22px; letter-spacing: 2px;">DUTY ROSTER</th>'
            "</tr>"
            # Year Sub-Header Row
            '<tr>'
            f'<th colspan="8" style="background-color: #ffffff; color: #cc0000; padding: 6px; text-align: center; border: 2px solid black; font-size: 18px; font-weight: bold;">{current_year}</th>'
            "</tr>"
            # Table Column Names Row
            '<tr style="background-color: #262626; color: white;">'
            '<th style="border: 2px solid black; padding: 8px; text-align: center; font-size: 15px;">Date</th>'
            '<th style="border: 2px solid black; padding: 8px; text-align: center; font-size: 15px;">Day</th>'
            '<th style="border: 2px solid black; padding: 8px; text-align: center; font-size: 15px;">Shift 1</th>'
            '<th style="border: 2px solid black; padding: 8px; text-align: center; font-size: 15px;">Shift 2</th>'
            '<th style="border: 2px solid black; padding: 8px; text-align: center; font-size: 15px;">Shift 3</th>'
            '<th style="border: 2px solid black; padding: 8px; text-align: center; font-size: 15px;">Shift 4</th>'
            '<th style="border: 2px solid black; padding: 8px; text-align: center; font-size: 15px;">OA-1</th>'
            '<th style="border: 2px solid black; padding: 8px; text-align: center; font-size: 15px;">OA-2</th>'
            "</tr>"
            "</thead>"
            "<tbody>"
        )

        for i in range(-8, 25):
            d = today + datetime.timedelta(days=i)
            day_diff = (d - base_date).days

            s_p = shift_pattern[day_diff % 8]
            o_p = oa_pattern[day_diff % 6]

            is_today = d == today
            bg_color = "#ffe6e6" if is_today else "#ffffff"
            text_color = "#cc0000" if is_today else "#000000"

            html_table += (
                f'<tr style="background-color: {bg_color}; color: {text_color}; font-weight: bold; text-align: center;">'
                f'<td style="border: 2px solid black; padding: 8px; font-size: 14px;">{d.strftime("%d-%b")}</td>'
                f'<td style="border: 2px solid black; padding: 8px; font-size: 14px;">{d.strftime("%A")}</td>'
                f'<td style="border: 2px solid black; padding: 8px; font-size: 14px;">{s_p["1"]}</td>'
                f'<td style="border: 2px solid black; padding: 8px; font-size: 14px;">{s_p["2"]}</td>'
                f'<td style="border: 2px solid black; padding: 8px; font-size: 14px;">{s_p["3"]}</td>'
                f'<td style="border: 2px solid black; padding: 8px; font-size: 14px;">{s_p["4"]}</td>'
                f'<td style="border: 2px solid black; padding: 8px; font-size: 14px;">{o_p["OA1"]}</td>'
                f'<td style="border: 2px solid black; padding: 8px; font-size: 14px;">{o_p["OA2"]}</td>'
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
                    f"{new_notice} (পোস্ট করেছেন: {st.session_state.user_name})"
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

    # --- মডিউল গ: এডমিন কন্ট্রোল (Shift Member Edit) ---
    elif menu == "এডমিন কন্ট্রোল (Shift & Member Edit)":
        st.header("🛠️ এডমিন প্যানেল: শিফট মেম্বার এডিট ও শিফট পরিবর্তন")
        st.info("কারো শিফট চেঞ্জ হলে এখান থেকে আপডেট করতে পারবেন।")

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("### ✏️ মেম্বারের শিফট পরিবর্তন করুন")
            selected_shift_from = st.selectbox(
                "বর্তমান শিফট সিলেক্ট করুন:",
                ["Shift 1", "Shift 2", "Shift 3", "Shift 4", "OA-1", "OA-2"],
            )
            member_list = st.session_state.shift_members[selected_shift_from]
            
            if member_list:
                selected_member = st.selectbox(
                    "মেম্বারের নাম সিলেক্ট করুন:", member_list
                )

                selected_shift_to = st.selectbox(
                    "নতুন কোন শিফটে নিতে চান?",
                    ["Shift 1", "Shift 2", "Shift 3", "Shift 4", "OA-1", "OA-2"],
                )

                if st.button("মেম্বারের শিফট আপডেট করুন"):
                    if selected_shift_from != selected_shift_to:
                        st.session_state.shift_members[selected_shift_from].remove(
                            selected_member
                        )
                        st.session_state.shift_members[selected_shift_to].append(
                            selected_member
                        )
                        st.success(
                            f"সফলভাবে {selected_member}-কে {selected_shift_from} থেকে {selected_shift_to}-এ ট্রান্সফার করা হয়েছে!"
                        )
                        st.rerun()
                    else:
                        st.warning("দয়া করে দুটি আলাদা ক্যাটাগরি সিলেক্ট করুন।")
            else:
                st.warning("এই শিফটে বর্তমানে কোনো সদস্য নেই।")

        with col_right:
            st.markdown("### 📝 সরাসরি সদস্যের নাম সংশোধন/এডিট")
            target_shift = st.selectbox(
                "শিফট নির্বাচন:",
                ["Shift 1", "Shift 2", "Shift 3", "Shift 4", "OA-1", "OA-2"],
                key="t_shift",
            )
            current_members = st.session_state.shift_members[target_shift]

            edited_members_str = st.text_area(
                "সদস্যদের নাম (প্রতি লাইনে একটি নাম লিখুন):",
                value="\n".join(current_members),
            )

            if st.button("তালিকা সেভ করুন"):
                new_list = [
                    name.strip()
                    for name in edited_members_str.split("\n")
                    if name.strip()
                ]
                st.session_state.shift_members[target_shift] = new_list
                st.success(f"{target_shift}-এর মেম্বার লিস্ট আপডেট হয়েছে!")
                st.rerun()