import json
from pathlib import Path

# Exact transcribed student answers from the 10 handwritten pages
STUDENT_HANDWRITTEN_PAGES = [
    {
        "page_number": 1,
        "filename": "page_001.jpg",
        "file_path": "/data/evaluation_demo/page_001.jpg",
        "transcription_markdown": """Law Test - 1

1) As per Section 2(6) of the Companies Act, 2013
-> An associate company, in relation to another company, means a company in which the other company has significant influence but not a subsidiary company but includes joint venture company.

Here,
- Alpha Ltd holds 22% voting power in a fiduciary capacity.
- But this 22% must be excluded while determining significant influence.
- It also holds 35% interest and participates in decisions under a joint venture agreement.

Conclusion,
- It qualifies as an Associate Company as the definition explicitly includes joint venture."""
    },
    {
        "page_number": 2,
        "filename": "page_002.jpg",
        "file_path": "/data/evaluation_demo/page_002.jpg",
        "transcription_markdown": """2) As per Sec 2(85) of the Companies Act, 2013
-> a "small company" means a company other than public company
- paid-up share capital does not exceed ten crore rupees
- turnover as per profit & loss account for the immediately preceding financial year does not exceed one hundred crore rupees.

Here,
- Zest Services Pvt. Ltd is a private company, its paid-up capital is 8 crore rupees which is within the limit.
- Also its turnover is 100 crore rupees which is also within the prescribed limit.
- But the definition of small company is not applicable to subsidiary company.

Conclusion,
- Zest Services Pvt Ltd qualifies as a small company but being a subsidiary it lose its status as small company."""
    },
    {
        "page_number": 3,
        "filename": "page_003.jpg",
        "file_path": "/data/evaluation_demo/page_003.jpg",
        "transcription_markdown": """3) As per the provisions of Companies Act, 2013
-> a natural person shall not be a member of more than one OPC at any point in time and shall not be a nominee of more than one OPC.
-> A member in an OPC becomes a member in another such company, such person shall meet the criteria within a period of 180 days.

Here,
- Aman was already a member of one OPC.
- By the death of Vikas on 1st October 2023, Aman became a member of the second OPC.
- This creates a situation of dual membership which is prohibited.

Conclusion,
- Aman must rectify the dual membership status within 180 days from 1st October 2023."""
    },
    {
        "page_number": 4,
        "filename": "page_004.jpg",
        "file_path": "/data/evaluation_demo/page_004.jpg",
        "transcription_markdown": """4) As per Section 16 of the Limited Liability Partnership (LLP) Act, 2008
-> A person may apply to the Registrar for reservation of a name in the following circumstances:
- As the name of a proposed LLP, or
- As the name to which an existing LLP proposes to change its name.

-> The application must be made in the prescribed form and manner along with prescribed fee.

-> Upon receiving such an application, the Registrar may reserve the name for a period of three months from the date of intimation by the Registrar.

-> No LLP shall be registered by a name which is
- undesirable, or
- identical or too nearly resembling to that of any other LLP or a company or registered trademark."""
    },
    {
        "page_number": 5,
        "filename": "page_005.jpg",
        "file_path": "/data/evaluation_demo/page_005.jpg",
        "transcription_markdown": """5) As per Section 31 of the Limited Liability Partnership (LLP) Act, 2008
-> The Court or Tribunal may reduce or waive any penalty leviable against any partner or employee of a LLP, if
- such partner or employee of an LLP has provided useful information during investigation
- when any information given by any partner or employee leads to LLP or any partner or employee of such LLP being convicted.

i) Yes, the Tribunal has power to waive or reduce the penalty of ₹1,25,000 being imposed on Mr. Aman as he has provided useful information.

ii) No partner or employee of any LLP may be discharged, demoted or suspended against the terms and conditions of his LLP or employment.
Hence Mr. Aman cannot be suspended from the job by the LLP."""
    },
    {
        "page_number": 6,
        "filename": "page_006.jpg",
        "file_path": "/data/evaluation_demo/page_006.jpg",
        "transcription_markdown": """6) As per Section 42 of the Companies Act, 2013
-> a company making an offer or invitation under private placement
- shall allot its securities within 60 days from the date of receipt of application
- if the company is unable to allot the securities within that period, it shall repay the application money with 15 days from the expiry of 60 days.
- if the company fails to repay, it is liable to repay that money with interest at the rate of 12% per annum from the expiry of 60th day.

Here,
- The application money from the members was received on 20th March 2023 and company did not make an allotment of share till 30th June 2023."""
    },
    {
        "page_number": 7,
        "filename": "page_007.jpg",
        "file_path": "/data/evaluation_demo/page_007.jpg",
        "transcription_markdown": """- Hence the company is liable to repay the amount along with 12% interest.

Conclusion,
- The objection raised by the members to non allotment of shares is valid but their claim to pay 15% interest is not valid."""
    },
    {
        "page_number": 8,
        "filename": "page_008.jpg",
        "file_path": "/data/evaluation_demo/page_008.jpg",
        "transcription_markdown": """7) As per Section 63 of the Companies Act, 2013
-> a company may issue fully paid-up bonus shares to its members out of
- Free Reserves
- Securities Premium
- Capital Redemption Reserve (CRR)
-> Bonus shares cannot be issued out of reserves created by revaluation of assets.
-> Bonus shares can be issued only when partly paid-up shares are made fully paid-up.

A) Particulars | ₹
CRR | 1,50,000
Securities Premium | 90,000
Surplus in Statement of Profit & Loss | 1,20,000
Total | 3,60,000"""
    },
    {
        "page_number": 9,
        "filename": "page_009.jpg",
        "file_path": "/data/evaluation_demo/page_009.jpg",
        "transcription_markdown": """B. Bonus Ratio -> 1:3
Bonus Shares = 90,000 * 1/3 = 30,000 shares
Face value -> ₹10
Amount = 30,000 * 10 = ₹3,00,000

C. No, the company cannot issue Bonus Shares until final call was made.
The partly paid-up shares shall be converted into fully paid-up to issue Bonus Shares."""
    },
    {
        "page_number": 10,
        "filename": "page_010.jpg",
        "file_path": "/data/evaluation_demo/page_010.jpg",
        "transcription_markdown": """8) As per the provisions of the Companies Act, 2013
-> Any amount received towards subscription to any securities including share application money is not a deposit.
-> If the securities for which application money was received cannot be allotted within 60 days from the date of receipt of application money and such application money is not refunded within 15 days, such amount shall be treated as a deposit.

Here,
- The company failed to allot security within 60 days and also failed to refund the money within 15 days grace period.

Conclusion,
- The amount of ₹3,00,000 will be treated as a deposit."""
    }
]

def main():
    dest = Path("backend/sample_data/evaluation/student_answers_demo.json")
    dest.write_text(json.dumps(STUDENT_HANDWRITTEN_PAGES, indent=2), encoding="utf-8")
    print(f"Saved demo student answers to {dest}")

if __name__ == "__main__":
    main()
