/**
 * Parallax Flow • CA Descriptive Answer AI Evaluator Pro
 * PRODUCTION FRONTEND CONTROLLER & STATE ENGINE
 * 
 * 1. Admin Authentication (View 1)
 * 2. Institute Executive Dashboard with Bento KPIs & Toppers (View 2)
 * 3. Student Profile & Enrolled Test Series (View 3)
 * 4. Ergonomic 2-Column Split Grading Workbench with Layout Presentation Step (View 4)
 * 5. Official Gazette Evaluation Report & PDF Download (View 5)
 */

(function () {
  'use strict';

  // ==========================================================================
  // 1. DATA STORE: STUDENTS, TESTS, AND EVALUATIONS
  // ==========================================================================
  const STUDENTS_DATA = [
    {
      id: 'stud_1',
      rollNo: '410892',
      regNo: 'WRO-0648291',
      name: 'Aarav Mehta',
      center: 'WIRC • Mumbai',
      region: 'WIRC',
      rank: 12,
      totalStudents: 80,
      cohort: 'May 2026 CA Final',
      aiStatus: 'AI Certified',
      aiConfidence: '99.4%',
      flagged: false,
      flagReason: null,
      flagDetails: null,
      tests: [
        { id: 'law1', name: 'Law Test - 1: Corporate & Other Laws', maxMarks: 42.0, awardedMarks: 34.5, status: 'Evaluated', submittedAt: '15m ago', pages: 6, flagged: false },
        { id: 'law2', name: 'Law Test - 2: Economic Laws & FEMA', maxMarks: 40.0, awardedMarks: null, status: 'In Queue', submittedAt: '2h ago', pages: 5, flagged: false },
        { id: 'audit1', name: 'Audit Test - 1: Professional Ethics & SA', maxMarks: 50.0, awardedMarks: null, status: 'Pending', submittedAt: 'Not Submitted', pages: 0, flagged: false }
      ]
    },
    {
      id: 'stud_2',
      rollNo: '410899',
      regNo: 'SRO-0518290',
      name: 'Tanvi Iyer',
      center: 'SIRC • Chennai',
      region: 'SIRC',
      rank: 1,
      totalStudents: 80,
      cohort: 'May 2026 CA Final',
      aiStatus: 'AI Certified',
      aiConfidence: '99.9%',
      flagged: false,
      flagReason: null,
      flagDetails: null,
      tests: [
        { id: 'law1', name: 'Law Test - 1: Corporate & Other Laws', maxMarks: 42.0, awardedMarks: 40.0, status: 'Evaluated', submittedAt: '42m ago', pages: 7, flagged: false }
      ]
    },
    {
      id: 'stud_3',
      rollNo: '410897',
      regNo: 'WRO-0629401',
      name: 'Devika Patel',
      center: 'WIRC • Ahmedabad',
      region: 'WIRC',
      rank: 2,
      totalStudents: 80,
      cohort: 'May 2026 CA Final',
      aiStatus: 'AI Certified',
      aiConfidence: '99.5%',
      flagged: false,
      flagReason: null,
      flagDetails: null,
      tests: [
        { id: 'law1', name: 'Law Test - 1: Corporate & Other Laws', maxMarks: 42.0, awardedMarks: 37.0, status: 'Evaluated', submittedAt: '1h ago', pages: 6, flagged: false }
      ]
    },
    {
      id: 'stud_4',
      rollNo: '410895',
      regNo: 'WRO-0610934',
      name: 'Ananya Desai',
      center: 'WIRC • Pune',
      region: 'WIRC',
      rank: 8,
      totalStudents: 80,
      cohort: 'May 2026 CA Final',
      aiStatus: 'AI Certified',
      aiConfidence: '98.9%',
      flagged: false,
      flagReason: null,
      flagDetails: null,
      tests: [
        { id: 'law1', name: 'Law Test - 1: Corporate & Other Laws', maxMarks: 42.0, awardedMarks: 32.0, status: 'Evaluated', submittedAt: '2h ago', pages: 6, flagged: false }
      ]
    },
    {
      id: 'stud_5',
      rollNo: '410896',
      regNo: 'SRO-0549102',
      name: 'Kabir Nair',
      center: 'SIRC • Kochi',
      region: 'SIRC',
      rank: 18,
      totalStudents: 80,
      cohort: 'May 2026 CA Final',
      aiStatus: 'AI Flagged',
      aiConfidence: '78.4%',
      flagged: true,
      flagReason: 'Borderline Cutoff (31.5/42) • Low OCR Legibility (Pg 3)',
      flagDetails: 'Candidate handwritten working on Page 3 (Section 186 ceiling limits) contains faint pencil corrections. AI scored 2.5/4.0 marks. Because the total score of 31.5/42 is on the 75% distinction boundary, autonomous seal was paused for administrative sign-off.',
      aiRecommendation: 'Confirm 2.5 marks awarded or accept candidate pencil working to award 3.0 marks.',
      tests: [
        { id: 'law1', name: 'Law Test - 1: Corporate & Other Laws', maxMarks: 42.0, awardedMarks: 31.5, status: 'Needs Review', submittedAt: '3h ago', pages: 5, flagged: true }
      ]
    },
    {
      id: 'stud_6',
      rollNo: '410898',
      regNo: 'NRO-0492810',
      name: 'Ishaan Verma',
      center: 'NIRC • New Delhi',
      region: 'NIRC',
      rank: 29,
      totalStudents: 80,
      cohort: 'May 2026 CA Final',
      aiStatus: 'AI Certified',
      aiConfidence: '98.6%',
      flagged: false,
      flagReason: null,
      flagDetails: null,
      tests: [
        { id: 'law1', name: 'Law Test - 1: Corporate & Other Laws', maxMarks: 42.0, awardedMarks: 28.0, status: 'Evaluated', submittedAt: '4h ago', pages: 6, flagged: false }
      ]
    },
    {
      id: 'stud_7',
      rollNo: '410901',
      regNo: 'NRO-0481902',
      name: 'Rohan Sharma',
      center: 'NIRC • Jaipur',
      region: 'NIRC',
      rank: 15,
      totalStudents: 80,
      cohort: 'May 2026 CA Final',
      aiStatus: 'AI Certified',
      aiConfidence: '99.1%',
      flagged: false,
      flagReason: null,
      flagDetails: null,
      tests: [
        { id: 'law1', name: 'Law Test - 1: Corporate & Other Laws', maxMarks: 42.0, awardedMarks: 33.0, status: 'Evaluated', submittedAt: '5h ago', pages: 6, flagged: false }
      ]
    },
    {
      id: 'stud_8',
      rollNo: '410905',
      regNo: 'SRO-0539180',
      name: 'Pooja Sundaram',
      center: 'SIRC • Bengaluru',
      region: 'SIRC',
      rank: 22,
      totalStudents: 80,
      cohort: 'May 2026 CA Final',
      aiStatus: 'AI Certified',
      aiConfidence: '99.0%',
      flagged: false,
      flagReason: null,
      flagDetails: null,
      tests: [
        { id: 'law1', name: 'Law Test - 1: Corporate & Other Laws', maxMarks: 42.0, awardedMarks: 30.5, status: 'Evaluated', submittedAt: '5h ago', pages: 5, flagged: false }
      ]
    },
    {
      id: 'stud_9',
      rollNo: '410912',
      regNo: 'WRO-0651982',
      name: 'Siddharth Joshi',
      center: 'WIRC • Surat',
      region: 'WIRC',
      rank: 34,
      totalStudents: 80,
      cohort: 'May 2026 CA Final',
      aiStatus: 'AI Flagged',
      aiConfidence: '74.8%',
      flagged: true,
      flagReason: 'Alternative Case-Law Cited • MCA Circular No. 04/2020',
      flagDetails: 'Candidate relied on general circular immunity (MCA Circular 04/2020) rather than the mandatory statutory proviso under Section 149(10) prescribed by ICAI Suggested Answers. AI awarded 1.5/4.0 marks on Q4.',
      aiRecommendation: 'Confirm 1.5/4.0 deduction as per benchmark or approve candidate alternative legal doctrine.',
      tests: [
        { id: 'law1', name: 'Law Test - 1: Corporate & Other Laws', maxMarks: 42.0, awardedMarks: 26.5, status: 'Needs Review', submittedAt: '6h ago', pages: 6, flagged: true }
      ]
    },
    {
      id: 'stud_10',
      rollNo: '410918',
      regNo: 'WRO-0638192',
      name: 'Meera Kulkarni',
      center: 'WIRC • Nagpur',
      region: 'WIRC',
      rank: 9,
      totalStudents: 80,
      cohort: 'May 2026 CA Final',
      aiStatus: 'AI Certified',
      aiConfidence: '99.4%',
      flagged: false,
      flagReason: null,
      flagDetails: null,
      tests: [
        { id: 'law1', name: 'Law Test - 1: Corporate & Other Laws', maxMarks: 42.0, awardedMarks: 35.0, status: 'Evaluated', submittedAt: '6h ago', pages: 7, flagged: false }
      ]
    }
  ];

  // TOPPERS LEADERBOARD (Top 5)
  const TOPPERS_LEADERBOARD = [
    { rank: 1, name: 'Tanvi Iyer', roll: '410899', score: '40.0 / 42.0', pct: '95.2%', tag: 'Statutory Mastery • Full Presentation Credit', studentId: 'stud_2' },
    { rank: 2, name: 'Devika Patel', roll: '410897', score: '37.0 / 42.0', pct: '88.1%', tag: 'Exemplary Working Notes Formulation', studentId: 'stud_3' },
    { rank: 3, name: 'Aarav Mehta', roll: '410892', score: '34.5 / 42.0', pct: '82.1%', tag: 'High Provision Precision & Case Reasoning', studentId: 'stud_1' },
    { rank: 4, name: 'Ananya Desai', roll: '410895', score: '32.0 / 42.0', pct: '76.2%', tag: 'Clear 3-Tier Statutory Structure', studentId: 'stud_4' },
    { rank: 5, name: 'Kabir Nair', roll: '410896', score: '31.5 / 42.0', pct: '75.0%', tag: 'Accurate Primary Legal Assertions', studentId: 'stud_5' }
  ];

  // ==========================================================================
  // 2. 100% ACCURATE BENCHMARK EXAM DATA: LAW TEST 1 (8 QUESTIONS)
  // INCLUDES DEDICATED ICAI LAYOUT & PRESENTATION STEP FOR EVERY QUESTION!
  // ==========================================================================
  const LAW_TEST_1_QUESTIONS = [
    {
      no: 1,
      code: 'Q.1',
      title: 'Associate Company & Joint Venture Test',
      sectionRef: 'Companies Act, 2013, Section 2(6)',
      maxMarks: 4.0,
      promptText: 'Alpha Ltd. holds 22% of the voting power in another company in a fiduciary capacity. It also holds a 35% interest in a joint venture agreement and participates in the decision-making process of the joint venture. Examine whether the company qualifies as an associate company under the provisions of the Companies Act, 2013.',
      studentText: `Answer to Question No. 1

1) As per Section 2(6) of the Companies Act, 2013:
-> An associate company, in relation to another company, means a company in which the other company has significant influence but not a subsidiary company but includes joint venture company.

Here,
- Alpha Ltd holds 22% voting power in a fiduciary capacity.
- But this 22% must be excluded while determining significant influence.
- It also holds 35% interest and participates in decisions under a joint venture agreement.

Conclusion:
- It qualifies as an Associate Company as the definition explicitly includes joint venture.`,
      icaiModelText: `Section 2(6) of the Companies Act, 2013 defines an associate company as a company in which that other company has significant influence, but which is not a subsidiary company, and expressly includes a joint venture company. Significant influence requires control of at least 20% of total voting power or participation in business decisions under an agreement. Voting power held in a fiduciary capacity is excluded. However, Alpha Ltd. holds 35% in a joint venture and participates in decisions. Therefore, the joint venture qualifies as an associate company.`,
      steps: [
        { stepNo: 1, title: 'Section 2(6) Citation & Definition', maxMarks: 1.0, marks: 1.0, feedback: 'Accurately cited Section 2(6) and defined significant influence.', tagsPresent: ['Section 2(6)', 'significant influence'], tagsMissing: [] },
        { stepNo: 2, title: 'Fiduciary Capacity Exclusion Rule', maxMarks: 1.0, marks: 1.0, feedback: 'Correctly noted that 22% fiduciary voting power cannot be counted.', tagsPresent: ['fiduciary capacity', 'excluded'], tagsMissing: [] },
        { stepNo: 3, title: 'Joint Venture Statutory Inclusion & Conclusion', maxMarks: 1.0, marks: 1.0, feedback: 'Unambiguous correct conclusion citing 35% JV participation.', tagsPresent: ['joint venture', 'participates in decisions'], tagsMissing: [] },
        { stepNo: 4, title: 'ICAI 3-Tier Layout & Drafting Presentation', maxMarks: 1.0, marks: 1.0, feedback: 'Exemplary 3-tier structure: Legal Provision -> Facts Analysis -> Definite Conclusion.', isPresentation: true, tagsPresent: ['3-tier format', 'margin numbering'], tagsMissing: [] }
      ]
    },
    {
      no: 2,
      code: 'Q.2',
      title: 'Small Company Definition & Subsidiary Exclusion',
      sectionRef: 'Companies Act, 2013, Section 2(85)',
      maxMarks: 4.0,
      promptText: 'Analyze whether Beta Pvt. Ltd. qualifies as a small company where its paid-up capital is Rs. 3 Crores and turnover is Rs. 35 Crores, but it is a subsidiary of a public company.',
      studentText: `Answer to Question No. 2

As per Section 2(85) of Companies Act, 2013:
Small company means a private company having:
- Paid up capital not exceeding Rs. 4 Crores.
- Turnover not exceeding Rs. 40 Crores.

Beta Pvt Ltd meets both limits (3 Cr < 4 Cr and 35 Cr < 40 Cr).
However, proviso to Section 2(85) states that a holding or subsidiary company can NEVER be a small company.

Conclusion:
Beta Pvt Ltd cannot be treated as a small company.`,
      icaiModelText: `Section 2(85) defines a small company as a private company whose paid-up share capital does not exceed Rs. 4 crore and turnover does not exceed Rs. 40 crore. However, clause (A) of the proviso states that nothing in this clause shall apply to a holding or subsidiary company. Since Beta Pvt. Ltd. is a subsidiary of a public company, it is statutorily excluded.`,
      steps: [
        { stepNo: 1, title: 'Section 2(85) Capital & Turnover Thresholds', maxMarks: 1.0, marks: 1.0, feedback: 'Correct statutory thresholds of Rs. 4 Crore and Rs. 40 Crore.', tagsPresent: ['Section 2(85)', 'Rs. 4 Crore', 'Rs. 40 Crore'], tagsMissing: [] },
        { stepNo: 2, title: 'Proviso Exception (Holding / Subsidiary)', maxMarks: 1.5, marks: 1.0, feedback: 'Applied subsidiary disqualification rule correctly.', tagsPresent: ['subsidiary company', 'proviso'], tagsMissing: ['clause (A)'] },
        { stepNo: 3, title: 'Direct Case Conclusion', maxMarks: 0.5, marks: 0.5, feedback: 'Accurately concluded Beta Pvt. Ltd. is not a small company.', tagsPresent: ['cannot be small company'], tagsMissing: [] },
        { stepNo: 4, title: 'ICAI 3-Tier Layout & Drafting Presentation', maxMarks: 1.0, marks: 0.5, feedback: 'Good structure; minor brevity in statutory clause explanation.', isPresentation: true, tagsPresent: ['clean headings'], tagsMissing: ['sub-rule reference'] }
      ]
    },
    {
      no: 3,
      code: 'Q.3',
      title: 'One Person Company (OPC) Dual Membership Restriction',
      sectionRef: 'Companies (Incorporation) Rules, 2014, Rule 3',
      maxMarks: 4.0,
      promptText: 'Mr. Ramesh is a sole member in an OPC. Can he incorporate another OPC or become a nominee in another OPC?',
      studentText: `Answer to Question No. 3

Rule 3 of Companies (Incorporation) Rules:
- A natural person who is an Indian citizen can incorporate only ONE One Person Company (OPC).
- He cannot be a member in more than one OPC at the same time.
- If he becomes member in another OPC by virtue of being nominee, he must withdraw within 180 days.

Hence, Mr. Ramesh cannot incorporate another OPC.`,
      icaiModelText: `Under Rule 3(2) of the Companies (Incorporation) Rules, 2014, a natural person shall not be eligible to incorporate more than one OPC or become nominee in more than one such company. Where a person becomes a member in another OPC by being a nominee, he shall meet the eligibility criteria within 180 days.`,
      steps: [
        { stepNo: 1, title: 'Rule 3 Natural Person & Citizenship Criteria', maxMarks: 1.0, marks: 1.0, feedback: 'Correct citation of Rule 3 and one OPC incorporation limit.', tagsPresent: ['Rule 3', 'only one OPC'], tagsMissing: [] },
        { stepNo: 2, title: '180-Day Nominee Transition Window', maxMarks: 1.5, marks: 1.0, feedback: 'Correctly noted the 180-day grace period to withdraw dual membership.', tagsPresent: ['180 days', 'nominee'], tagsMissing: [] },
        { stepNo: 3, title: 'Direct Prohibition Conclusion', maxMarks: 0.5, marks: 0.5, feedback: 'Accurate conclusion on restriction.', tagsPresent: ['cannot incorporate another'], tagsMissing: [] },
        { stepNo: 4, title: 'ICAI 3-Tier Layout & Drafting Presentation', maxMarks: 1.0, marks: 0.5, feedback: 'Clear bulleted format; missed explicit sub-rule 3(2) citation.', isPresentation: true, tagsPresent: ['clear bullets'], tagsMissing: ['Rule 3(2) citation'] }
      ]
    },
    {
      no: 4,
      code: 'Q.4',
      title: 'Reservation of Name of LLP & 3-Month Window',
      sectionRef: 'LLP Act, 2008, Section 16 & Rule 18',
      maxMarks: 8.0,
      promptText: 'Explain the procedure and timeline for reservation of name of an LLP under Section 16 of the LLP Act, 2008.',
      studentText: `Answer to Question No. 4

Under Section 16 of the LLP Act, 2008:
1. Application for reservation of name is made via RUN-LLP (Reserve Unique Name) form with prescribed fee.
2. Registrar reserves name for 3 months from intimation date.
3. The proposed name must not be undesirable or identical to existing company/LLP or registered trademark.

If not incorporated within 3 months, reservation lapses.`,
      icaiModelText: `Section 16 of the LLP Act, 2008 read with Rule 18 provides that a person may apply in the prescribed form and manner accompanied by fees to the Registrar for name reservation. Upon payment, the Registrar may reserve the name for a period of 3 months from the date of intimation. The name must not be undesirable or identical to any other partnership, LLP, company, or trademark.`,
      steps: [
        { stepNo: 1, title: 'Section 16 Application & RUN-LLP Procedure', maxMarks: 2.0, marks: 2.0, feedback: 'Correct application procedure and fee requirements.', tagsPresent: ['Section 16', 'Registrar', 'RUN-LLP'], tagsMissing: [] },
        { stepNo: 2, title: '3-Month Statutory Validity Window', maxMarks: 2.5, marks: 2.0, feedback: 'Accurately stated 3-month validity duration from intimation.', tagsPresent: ['3 months', 'reservation lapses'], tagsMissing: ['date of intimation'] },
        { stepNo: 3, title: 'Name Undesirability & Trademark Prohibitions', maxMarks: 2.0, marks: 1.5, feedback: 'Covered identical names and trademarks; missed Emblems Act reference.', tagsPresent: ['undesirable', 'trademark', 'identical'], tagsMissing: ['Emblems and Names Act'] },
        { stepNo: 4, title: 'ICAI 3-Tier Layout & Drafting Presentation', maxMarks: 1.5, marks: 0.5, feedback: 'Good procedural numbered sequence; lacked separate facts-law breakdown.', isPresentation: true, tagsPresent: ['sequential numbering'], tagsMissing: ['elaborate legal commentary'] }
      ]
    },
    {
      no: 5,
      code: 'Q.5',
      title: 'LLP Whistleblowing Protection & Penalty Waiver',
      sectionRef: 'LLP Act, 2008, Section 31',
      maxMarks: 6.0,
      promptText: 'Discuss the whistleblowing provisions under Section 31 of the LLP Act, 2008 and conditions under which penalty is waived.',
      studentText: `Answer to Question No. 5

Section 31 of LLP Act, 2008 deals with Whistle Blowing:
- Court/Tribunal may reduce or waive penalty on a partner or employee if:
  1) They provided useful information during investigation of the LLP.
  2) When any information is given which leads to LLP or any partner being convicted.
- No partner or employee shall be demoted, suspended, or harassed for whistleblowing.`,
      icaiModelText: `Section 31 provides protection to whistleblowers. The Court or Tribunal may reduce or waive any penalty leviable against any partner or employee of an LLP if satisfied that such partner or employee has provided useful information during investigation or when information leads to conviction. Further, such whistleblower cannot be discharged, demoted, suspended, threatened, or harassed.`,
      steps: [
        { stepNo: 1, title: 'Section 31 Court/Tribunal Power of Waiver', maxMarks: 1.5, marks: 1.5, feedback: 'Accurate statement on Tribunal/Court reduction powers.', tagsPresent: ['Section 31', 'Court or Tribunal', 'waive penalty'], tagsMissing: [] },
        { stepNo: 2, title: 'Substantive Conditions (Investigation & Conviction)', maxMarks: 2.0, marks: 1.5, feedback: 'Both conditions cited clearly.', tagsPresent: ['useful information', 'leads to conviction'], tagsMissing: [] },
        { stepNo: 3, title: 'Anti-Victimization / Retaliation Protection', maxMarks: 1.5, marks: 1.0, feedback: 'Covered harassment, suspension, and demotion.', tagsPresent: ['demoted', 'suspended', 'harassed'], tagsMissing: ['discharged'] },
        { stepNo: 4, title: 'ICAI 3-Tier Layout & Drafting Presentation', maxMarks: 1.0, marks: 0.5, feedback: 'Clear bullet points with statutory grounding.', isPresentation: true, tagsPresent: ['bullet format'], tagsMissing: ['detailed case analysis'] }
      ]
    },
    {
      no: 6,
      code: 'Q.6',
      title: 'Private Placement 60-Day Allotment & 12% Interest',
      sectionRef: 'Companies Act, 2013, Section 42(6)',
      maxMarks: 4.0,
      promptText: 'A company failed to allot shares within 60 days of receiving application money under private placement. State the statutory consequence and interest liability.',
      studentText: `Answer to Question No. 6

As per Section 42(6) of Companies Act, 2013:
- Company must allot securities within 60 days of receiving application money.
- If not allotted within 60 days, it must repay the application money within 15 days from the expiry of 60 days.
- If not repaid within 15 days, it is liable to repay with interest at 12% per annum from the 60th day.`,
      icaiModelText: `Section 42(6) mandates that a company making an offer or invitation under private placement shall allot its securities within sixty days from the date of receipt of the application money. If not allotted, the application money must be repaid within fifteen days from the expiry of sixty days. Failure to repay triggers interest at 12% per annum from the expiry of the sixtieth day.`,
      steps: [
        { stepNo: 1, title: '60-Day Mandatory Allotment Timeline', maxMarks: 1.0, marks: 1.0, feedback: 'Correct statement of 60-day allotment period.', tagsPresent: ['Section 42(6)', '60 days'], tagsMissing: [] },
        { stepNo: 2, title: '15-Day Repayment Grace Window', maxMarks: 1.0, marks: 1.0, feedback: 'Accurately stated 15-day refund deadline.', tagsPresent: ['repay within 15 days'], tagsMissing: [] },
        { stepNo: 3, title: '12% p.a. Interest Penalty Accrual Rule', maxMarks: 1.0, marks: 0.5, feedback: 'Noted 12% rate; missed clarifying interest accrues from the 60th day.', tagsPresent: ['12% per annum'], tagsMissing: ['accrues from 60th day'] },
        { stepNo: 4, title: 'ICAI 3-Tier Layout & Drafting Presentation', maxMarks: 1.0, marks: 0.5, feedback: 'Well structured; minor drafting brevity on statutory dates.', isPresentation: true, tagsPresent: ['timeline breakdown'], tagsMissing: ['full case computation'] }
      ]
    },
    {
      no: 7,
      code: 'Q.7',
      title: 'Issue of Bonus Shares from CRR & Free Reserves',
      sectionRef: 'Companies Act, 2013, Section 63',
      maxMarks: 8.0,
      promptText: 'Explain the sources from which bonus shares can be issued under Section 63 and conditions to be complied with.',
      studentText: `Answer to Question No. 7

Section 63 of Companies Act, 2013:
A company may issue fully paid-up bonus shares out of:
1. Its free reserves.
2. The securities premium account.
3. The Capital Redemption Reserve (CRR) account.

Proviso: Bonus shares shall NOT be issued by capitalizing reserves created by revaluation of assets.

Conditions:
- Authorized by Articles of Association (AOA).
- Recommended by Board and approved in General Meeting.
- No default in payment of interest or principal of fixed deposits/debt securities.
- No default in statutory dues of employees (PF, gratuity, bonus).
- Partly paid-up shares must be made fully paid-up.
- Bonus shares once announced cannot be withdrawn.`,
      icaiModelText: `Section 63(1) permits issue of bonus shares out of free reserves, securities premium account, or Capital Redemption Reserve. Capitalizing revaluation reserves is expressly prohibited. Section 63(2) prescribes authorization in Articles, approval in General Meeting, no default in debt/deposits or employee dues, partly paid shares made fully paid, and irrevocability of recommendation.`,
      steps: [
        { stepNo: 1, title: 'Permissible Sources (Free Reserves, SP, CRR)', maxMarks: 2.5, marks: 2.5, feedback: 'All 3 sources identified correctly.', tagsPresent: ['free reserves', 'securities premium', 'Capital Redemption Reserve'], tagsMissing: [] },
        { stepNo: 2, title: 'Revaluation Reserve Prohibition Proviso', maxMarks: 1.5, marks: 1.5, feedback: 'Correctly noted prohibition on capitalizing revaluation reserve.', tagsPresent: ['revaluation of assets', 'prohibited'], tagsMissing: [] },
        { stepNo: 3, title: 'Section 63(2) Pre-Conditions & Defaults Check', maxMarks: 2.5, marks: 2.5, feedback: 'Comprehensive coverage of AOA, employee dues, and debt checks.', tagsPresent: ['Articles of Association', 'employee dues', 'cannot be withdrawn'], tagsMissing: [] },
        { stepNo: 4, title: 'ICAI 3-Tier Layout & Drafting Presentation', maxMarks: 1.5, marks: 1.5, feedback: 'Flawless presentation, clear numbered conditions, perfect legal citations.', isPresentation: true, tagsPresent: ['flawless format', 'underlined headings'], tagsMissing: [] }
      ]
    },
    {
      no: 8,
      code: 'Q.8',
      title: 'Share Application Money & 60-Day Deemed Deposit Rule',
      sectionRef: 'Companies (Acceptance of Deposits) Rules, 2014, Rule 2(1)(c)',
      maxMarks: 4.0,
      promptText: 'Examine when share application money is deemed as a deposit under the Companies Act, 2013.',
      studentText: `Answer to Question No. 8

Under Companies (Acceptance of Deposits) Rules, 2014:
- Any amount received towards share application money is not a deposit IF securities are allotted within 60 days.
- If not allotted within 60 days and not refunded within 15 days from expiry of 60 days, it shall be treated as a DEPOSIT.
- It will be treated as deposit from the 75th day of receipt.`,
      icaiModelText: `Under Rule 2(1)(c)(vii) of the Companies (Acceptance of Deposits) Rules, 2014, any amount received towards application for securities is excluded from deposits if securities are allotted within 60 days. If not allotted and not refunded within 15 days following the expiry of 60 days, such amount shall be treated as a deposit after the expiry of 15 days (i.e. from the 76th day).`,
      steps: [
        { stepNo: 1, title: 'Initial Exclusion of Application Money', maxMarks: 1.0, marks: 1.0, feedback: 'Correctly noted exclusion if allotted in 60 days.', tagsPresent: ['60 days', 'application money'], tagsMissing: [] },
        { stepNo: 2, title: '15-Day Refund Window & Deemed Deposit', maxMarks: 1.5, marks: 1.0, feedback: 'Identified deemed deposit after 15-day refund window.', tagsPresent: ['treated as deposit', '15 days'], tagsMissing: ['Rule 2(1)(c)(vii)'] },
        { stepNo: 3, title: 'Statutory Effective Date of Deposit', maxMarks: 0.5, marks: 0.5, feedback: 'Correct operational timeline.', tagsPresent: ['effective date'], tagsMissing: [] },
        { stepNo: 4, title: 'ICAI 3-Tier Layout & Drafting Presentation', maxMarks: 1.0, marks: 0.5, feedback: 'Clear concise structure; missed full rule sub-clause reference.', isPresentation: true, tagsPresent: ['clean summary'], tagsMissing: ['sub-clause citation'] }
      ]
    }
  ];

  // ==========================================================================
  // 3. APPLICATION STATE
  // ==========================================================================
  let activeView = 'dashboard'; // 'login' | 'dashboard' | 'student-profile' | 'workbench' | 'report'
  let activeStudent = STUDENTS_DATA[0]; // Aarav Mehta
  let activeTestId = 'law1';
  let activeQuestionIndex = 0; // 0 to 7 (Q.1 to Q.8)
  let activeMode = 'ocr'; // 'ocr' | 'diff' | 'scan'
  let currentSearchQuery = '';
  let activeDashFilter = 'ALL'; // 'ALL' | 'CERTIFIED' | 'FLAGGED'

  // DOM Elements Cache
  const dom = {};

  // Toast Notification Helper
  function showToast(message, isError = false) {
    if (!dom.toast) return;
    if (dom.toastMsg) dom.toastMsg.textContent = message;
    const toastIcon = document.getElementById('toast-icon');
    if (toastIcon) {
      toastIcon.innerHTML = isError
        ? `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`
        : `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>`;
    }
    dom.toast.classList.add('show');
    setTimeout(() => {
      dom.toast.classList.remove('show');
    }, 3500);
  }

  // ==========================================================================
  // 4. INITIALIZATION
  // ==========================================================================
  function init() {
    cacheDom();
    bindEvents();
    renderDashboard();
    renderWorkbenchQuestion(0);
    renderReport();
    switchView('login'); // Starts directly on Admin Login screen!
  }

  function cacheDom() {
    // Views
    dom.viewLogin = document.getElementById('view-login');
    dom.viewDashboard = document.getElementById('view-dashboard');
    dom.viewStudentProfile = document.getElementById('view-student-profile');
    dom.viewWorkbench = document.getElementById('view-workbench');
    dom.viewReport = document.getElementById('view-report');

    // Top Nav
    dom.topNav = document.getElementById('pf-nav-wrapper');
    dom.navBrandLogo = document.getElementById('nav-brand-logo');
    dom.navLinkDash = document.getElementById('nav-link-dash');
    dom.navLinkStudents = document.getElementById('nav-link-students');
    dom.navLinkWorkbench = document.getElementById('nav-link-workbench');
    dom.navLinkReport = document.getElementById('nav-link-report');
    dom.btnLogout = document.getElementById('btn-logout');

    // Dashboard
    dom.dashSubmissionsTbody = document.getElementById('dash-submissions-tbody');
    dom.dashToppersList = document.getElementById('dash-toppers-list');
    dom.dashStudentSearch = document.getElementById('dash-student-search');
    dom.dashSearchClear = document.getElementById('dash-search-clear');
    dom.dashSubmissionsCount = document.getElementById('dash-submissions-count');
    dom.btnDashOpenDirectory = document.getElementById('btn-dash-open-directory');
    dom.dashAiFilterTabs = document.getElementById('dash-ai-filter-tabs');
    dom.btnTriggerAiBatch = document.getElementById('btn-trigger-ai-batch');
    dom.modalAiBatch = document.getElementById('modal-ai-batch');
    dom.btnCloseBatchModal = document.getElementById('btn-close-batch-modal');
    dom.btnFinishBatchModal = document.getElementById('btn-finish-batch-modal');

    // Overall Student Master Directory & Dossier
    dom.studentDirectoryContainer = document.getElementById('student-directory-container');
    dom.studentDetailContainer = document.getElementById('student-detail-container');
    dom.masterStudentsTbody = document.getElementById('master-students-tbody');
    dom.masterStudentCount = document.getElementById('master-student-count');
    dom.dirStudentSearch = document.getElementById('dir-student-search');
    dom.dirSearchClear = document.getElementById('dir-search-clear');
    dom.dirFilterRegion = document.getElementById('dir-filter-region');
    dom.dirFilterStatus = document.getElementById('dir-filter-status');
    dom.btnExportStudentsCsv = document.getElementById('btn-export-students-csv');
    dom.btnBackToDirectory = document.getElementById('btn-back-to-directory');
    dom.btnProfileOpenWb = document.getElementById('btn-profile-open-wb');

    // Individual Student Profile Detail
    dom.profName = document.getElementById('prof-name');
    dom.profRoll = document.getElementById('prof-roll');
    dom.profReg = document.getElementById('prof-reg');
    dom.profCenter = document.getElementById('prof-center');
    dom.profRank = document.getElementById('prof-rank');
    dom.profAvatar = document.getElementById('prof-avatar');
    dom.profTestsGrid = document.getElementById('prof-tests-grid');
    dom.btnBackFromProfile = document.getElementById('btn-back-from-profile');

    // Workbench
    dom.ribbonTrack = document.getElementById('ribbon-track');
    dom.btnPrevQ = document.getElementById('btn-prev-q');
    dom.btnNextQ = document.getElementById('btn-next-q');
    dom.qPagerLabel = document.getElementById('q-pager-label');
    dom.wbAiFlagContainer = document.getElementById('wb-ai-flag-container');

    dom.wbPromptCode = document.getElementById('wb-prompt-code');
    dom.wbPromptSection = document.getElementById('wb-prompt-section');
    dom.wbPromptMarks = document.getElementById('wb-prompt-marks');
    dom.wbPromptTitle = document.getElementById('wb-prompt-title');
    dom.wbPromptText = document.getElementById('wb-prompt-text');

    dom.wbOcrCard = document.getElementById('wb-ocr-card');
    dom.wbDiffCard = document.getElementById('wb-diff-card');
    dom.wbScanCard = document.getElementById('wb-scan-card');
    dom.wbTranscriptBody = document.getElementById('wb-transcript-body');
    dom.wbDiffBody = document.getElementById('wb-diff-body');
    dom.wbScanBody = document.getElementById('wb-scan-body');

    dom.wbRubricTitle = document.getElementById('wb-rubric-title');
    dom.wbQscorePill = document.getElementById('wb-qscore-pill');
    dom.wbStepCardsContainer = document.getElementById('wb-step-cards-container');
    dom.btnWbViewReport = document.getElementById('btn-wb-view-report');

    // Toast
    dom.toast = document.getElementById('pf-toast');
    dom.toastMsg = document.getElementById('toast-msg');

    // Report
    dom.btnReportBackWb = document.getElementById('btn-report-back-wb');
    dom.btnReportPrint = document.getElementById('btn-report-print');
    dom.repName = document.getElementById('rep-name');
    dom.repRoll = document.getElementById('rep-roll');
    dom.repPaper = document.getElementById('rep-paper');
    dom.repScoreHuge = document.getElementById('rep-score-huge');
    dom.repExecTbody = document.getElementById('rep-exec-tbody');
    dom.repQuestionsAuditTrail = document.getElementById('rep-questions-audit-trail');
  }

  // ==========================================================================
  // 5. VIEW SWITCHING
  // ==========================================================================
  function switchView(targetView, student = null) {
    activeView = targetView;

    // Hide all views
    [dom.viewLogin, dom.viewDashboard, dom.viewStudentProfile, dom.viewWorkbench, dom.viewReport].forEach(v => {
      if (v) v.classList.remove('active');
    });

    // Reset active nav links
    [dom.navLinkDash, dom.navLinkStudents, dom.navLinkWorkbench, dom.navLinkReport].forEach(l => {
      if (l) l.classList.remove('active');
    });

    if (targetView === 'login') {
      if (dom.viewLogin) dom.viewLogin.classList.add('active');
      if (dom.topNav) dom.topNav.style.display = 'none';
    } else {
      if (dom.topNav) dom.topNav.style.display = 'flex';
      if (targetView === 'dashboard') {
        if (dom.viewDashboard) dom.viewDashboard.classList.add('active');
        if (dom.navLinkDash) dom.navLinkDash.classList.add('active');
      } else if (targetView === 'student-profile') {
        if (dom.viewStudentProfile) dom.viewStudentProfile.classList.add('active');
        if (dom.navLinkStudents) dom.navLinkStudents.classList.add('active');
        if (student) {
          showStudentDetail(student);
        } else {
          showStudentDirectory();
        }
      } else if (targetView === 'workbench') {
        if (dom.viewWorkbench) dom.viewWorkbench.classList.add('active');
        renderWorkbenchQuestion(activeQuestionIndex);
        if (dom.navLinkWorkbench) dom.navLinkWorkbench.classList.add('active');
      } else if (targetView === 'report') {
        if (dom.viewReport) dom.viewReport.classList.add('active');
        renderReport();
        if (dom.navLinkReport) dom.navLinkReport.classList.add('active');
      }
    }
  }

  // ==========================================================================
  // 6. EVENT BINDINGS
  // ==========================================================================
  function bindEvents() {
    // Login form submit
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        switchView('dashboard');
      });
    }

    // Top Nav buttons
    if (dom.navBrandLogo) dom.navBrandLogo.addEventListener('click', () => switchView('dashboard'));
    if (dom.navLinkDash) dom.navLinkDash.addEventListener('click', () => switchView('dashboard'));
    if (dom.navLinkStudents) dom.navLinkStudents.addEventListener('click', () => switchView('student-profile'));
    if (dom.navLinkWorkbench) dom.navLinkWorkbench.addEventListener('click', () => switchView('workbench'));
    if (dom.navLinkReport) dom.navLinkReport.addEventListener('click', () => switchView('report'));
    if (dom.btnLogout) dom.btnLogout.addEventListener('click', () => switchView('login'));
    if (dom.btnBackFromProfile) dom.btnBackFromProfile.addEventListener('click', () => switchView('dashboard'));

    // Question Ribbon Pager
    if (dom.btnPrevQ) {
      dom.btnPrevQ.addEventListener('click', () => {
        if (activeQuestionIndex > 0) {
          activeQuestionIndex--;
          renderWorkbenchQuestion(activeQuestionIndex);
        }
      });
    }

    if (dom.btnNextQ) {
      dom.btnNextQ.addEventListener('click', () => {
        if (activeQuestionIndex < LAW_TEST_1_QUESTIONS.length - 1) {
          activeQuestionIndex++;
          renderWorkbenchQuestion(activeQuestionIndex);
        }
      });
    }

    // Mode segmented buttons (Transcribed, Model Answer Diff, Scan)
    const modeBtns = document.querySelectorAll('.pf-mode-btn');
    modeBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        modeBtns.forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        activeMode = btn.dataset.mode;
        updateCenterModeDisplay();
      });
    });

    // Workbench -> Report buttons
    if (dom.btnWbViewReport) dom.btnWbViewReport.addEventListener('click', () => switchView('report'));
    if (dom.btnReportBackWb) dom.btnReportBackWb.addEventListener('click', () => switchView('workbench'));
    if (dom.btnReportPrint) dom.btnReportPrint.addEventListener('click', () => window.print());

    // Keyboard Shortcuts (Arrow keys for question navigation)
    window.addEventListener('keydown', (e) => {
      if (activeView === 'workbench') {
        if (e.key === 'ArrowRight' && activeQuestionIndex < LAW_TEST_1_QUESTIONS.length - 1) {
          activeQuestionIndex++;
          renderWorkbenchQuestion(activeQuestionIndex);
        } else if (e.key === 'ArrowLeft' && activeQuestionIndex > 0) {
          activeQuestionIndex--;
          renderWorkbenchQuestion(activeQuestionIndex);
        }
      }
    });
    // Search input & clear button
    if (dom.dashStudentSearch) {
      dom.dashStudentSearch.addEventListener('input', (e) => {
        currentSearchQuery = e.target.value;
        if (dom.dashSearchClear) {
          dom.dashSearchClear.style.display = currentSearchQuery ? 'grid' : 'none';
        }
        renderDashboard(currentSearchQuery);
      });
      dom.dashStudentSearch.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          dom.dashStudentSearch.value = '';
          currentSearchQuery = '';
          if (dom.dashSearchClear) dom.dashSearchClear.style.display = 'none';
          renderDashboard('');
        }
      });
    }

    if (dom.dashSearchClear) {
      dom.dashSearchClear.addEventListener('click', () => {
        if (dom.dashStudentSearch) {
          dom.dashStudentSearch.value = '';
          dom.dashStudentSearch.focus();
        }
        currentSearchQuery = '';
        dom.dashSearchClear.style.display = 'none';
        renderDashboard('');
      });
    }

    // Dashboard -> Open Master Directory
    if (dom.btnDashOpenDirectory) {
      dom.btnDashOpenDirectory.addEventListener('click', () => {
        switchView('student-profile');
      });
    }

    // Directory Search & Clear
    if (dom.dirStudentSearch) {
      dom.dirStudentSearch.addEventListener('input', () => {
        const val = dom.dirStudentSearch.value;
        if (dom.dirSearchClear) dom.dirSearchClear.style.display = val ? 'grid' : 'none';
        renderMasterDirectory();
      });
      dom.dirStudentSearch.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          dom.dirStudentSearch.value = '';
          if (dom.dirSearchClear) dom.dirSearchClear.style.display = 'none';
          renderMasterDirectory();
        }
      });
    }

    if (dom.dirSearchClear) {
      dom.dirSearchClear.addEventListener('click', () => {
        if (dom.dirStudentSearch) {
          dom.dirStudentSearch.value = '';
          dom.dirStudentSearch.focus();
        }
        dom.dirSearchClear.style.display = 'none';
        renderMasterDirectory();
      });
    }

    // Directory Region & Status Dropdown Filters
    if (dom.dirFilterRegion) {
      dom.dirFilterRegion.addEventListener('change', () => {
        renderMasterDirectory();
      });
    }

    if (dom.dirFilterStatus) {
      dom.dirFilterStatus.addEventListener('change', () => {
        renderMasterDirectory();
      });
    }

    // Export Master CSV
    if (dom.btnExportStudentsCsv) {
      dom.btnExportStudentsCsv.addEventListener('click', () => {
        exportStudentsCsv();
      });
    }

    // Candidate Dossier -> Back to Directory
    if (dom.btnBackToDirectory) {
      dom.btnBackToDirectory.addEventListener('click', () => {
        showStudentDirectory();
      });
    }

    // Candidate Dossier -> Open Evaluator Workbench
    if (dom.btnProfileOpenWb) {
      dom.btnProfileOpenWb.addEventListener('click', () => {
        switchView('workbench');
      });
    }

    // AI Autonomy Filter Tabs (All / Certified / Flagged)
    if (dom.dashAiFilterTabs) {
      const tabBtns = dom.dashAiFilterTabs.querySelectorAll('.pf-mode-btn');
      tabBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
          tabBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          activeDashFilter = btn.dataset.filter;
          renderDashboard();
        });
      });
    }

    // AI Batch Ingestion Modal
    if (dom.btnTriggerAiBatch && dom.modalAiBatch) {
      dom.btnTriggerAiBatch.addEventListener('click', () => {
        dom.modalAiBatch.classList.add('open');
      });
    }

    if (dom.btnCloseBatchModal && dom.modalAiBatch) {
      dom.btnCloseBatchModal.addEventListener('click', () => {
        dom.modalAiBatch.classList.remove('open');
      });
    }

    if (dom.btnFinishBatchModal && dom.modalAiBatch) {
      dom.btnFinishBatchModal.addEventListener('click', () => {
        dom.modalAiBatch.classList.remove('open');
        showToast('Autonomous ingestion complete: 80 papers verified, 20 exceptions routed to audit queue.');
        renderDashboard();
      });
    }
  }

  // ==========================================================================
  // 7. DASHBOARD RENDERING (Live Feed + Toppers + Search)
  // ==========================================================================
  function highlightMatch(text, query) {
    if (!query) return text;
    const safe = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${safe})`, 'gi');
    return text.replace(regex, '<mark class="pf-search-highlight">$1</mark>');
  }

  function renderDashboard(query = currentSearchQuery) {
    const q = (query || '').trim().toLowerCase();

    // Filter students by Name, Roll Number, or Exam Center + AI Autonomy filter
    const filteredStudents = STUDENTS_DATA.filter((s) => {
      // 1. Search Query
      if (q) {
        const matchName = s.name.toLowerCase().includes(q);
        const matchRoll = s.rollNo.toLowerCase().includes(q);
        const matchCenter = s.center.toLowerCase().includes(q);
        if (!matchName && !matchRoll && !matchCenter) return false;
      }
      // 2. AI Autonomy Filter
      const test = s.tests.find((t) => t.id === 'law1') || s.tests[0];
      const isFlagged = test && test.flagged;
      if (activeDashFilter === 'CERTIFIED' && isFlagged) return false;
      if (activeDashFilter === 'FLAGGED' && !isFlagged) return false;

      return true;
    });

    // Update submissions count pill
    if (dom.dashSubmissionsCount) {
      if (q) {
        dom.dashSubmissionsCount.textContent = `${filteredStudents.length} of ${STUDENTS_DATA.length} Found`;
      } else if (activeDashFilter === 'CERTIFIED') {
        dom.dashSubmissionsCount.textContent = `80 AI Certified`;
      } else if (activeDashFilter === 'FLAGGED') {
        dom.dashSubmissionsCount.textContent = `20 AI Flagged`;
      } else {
        dom.dashSubmissionsCount.textContent = `100 Ingested`;
      }
    }

    // 1. Live Submissions Table
    dom.dashSubmissionsTbody.innerHTML = '';

    if (filteredStudents.length === 0) {
      dom.dashSubmissionsTbody.innerHTML = `
        <tr>
          <td colspan="6" style="text-align: center; padding: 40px 16px; color: var(--pf-muted);">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 6px; opacity: 0.5;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <div style="font-weight: 700; color: var(--pf-ink); font-size: 13.5px;">No papers matching current filter criteria</div>
            <div style="font-size: 11px; margin-top: 4px; color: var(--pf-muted);">
              Try resetting the AI telemetry status tabs or clear the search query.
            </div>
            <button type="button" class="btn-table-review" id="btn-empty-clear-search" style="margin-top: 10px; display: inline-flex;">
              Reset Filters
            </button>
          </td>
        </tr>
      `;
      const emptyClearBtn = document.getElementById('btn-empty-clear-search');
      if (emptyClearBtn) {
        emptyClearBtn.addEventListener('click', () => {
          if (dom.dashStudentSearch) dom.dashStudentSearch.value = '';
          currentSearchQuery = '';
          if (dom.dashSearchClear) dom.dashSearchClear.style.display = 'none';
          activeDashFilter = 'ALL';
          if (dom.dashAiFilterTabs) {
            dom.dashAiFilterTabs.querySelectorAll('.pf-mode-btn').forEach((b, i) => {
              b.classList.toggle('active', i === 0);
            });
          }
          renderDashboard('');
        });
      }
    } else {
      filteredStudents.forEach((s) => {
        const test = s.tests.find((t) => t.id === 'law1') || s.tests[0];
        const tr = document.createElement('tr');

        const isFlagged = test && test.flagged;
        const scoreDisplay = test && test.awardedMarks !== null ? `${test.awardedMarks.toFixed(1)} / ${test.maxMarks.toFixed(1)}` : 'In Queue...';

        const displayName = q ? highlightMatch(s.name, q) : s.name;
        const displayRoll = q ? highlightMatch(s.rollNo, q) : s.rollNo;
        const displayCenter = q ? highlightMatch(s.center, q) : s.center;

        const statusHtml = !isFlagged
          ? `<span class="pf-telemetry-badge verified"><span class="pf-telemetry-dot verified"></span>Autonomous Verified <span class="font-mono text-xs" style="opacity: 0.75; margin-left: 2px;">${s.aiConfidence || '99.4%'}</span></span>`
          : `<div class="pf-ai-flag-group">
               <span class="pf-telemetry-badge exception"><span class="pf-telemetry-dot exception"></span>Audit Exception</span>
               <span class="pf-ai-reason-tag font-mono" title="${s.flagReason || ''}">${s.flagReason || 'Requires Admin Clearance'}</span>
             </div>`;

        const actionBtn = isFlagged
          ? `<button class="btn-table-resolve" data-student-id="${s.id}"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg> Clear Exception &rarr;</button>`
          : `<button class="btn-table-review" data-student-id="${s.id}">Audit Trail &rarr;</button>`;

        tr.innerHTML = `
          <td>
            <div class="student-col-info">
              <div class="student-table-avatar">${s.name.split(' ').map(n=>n[0]).join('')}</div>
              <div>
                <div class="student-name-text" data-student-id="${s.id}">${displayName}</div>
                <div class="student-roll-tag font-mono">Roll: ${displayRoll} • ${displayCenter}</div>
              </div>
            </div>
          </td>
          <td class="font-mono text-muted">${test.submittedAt}</td>
          <td class="font-mono">${test.pages} pgs</td>
          <td class="font-mono font-bold" style="text-align: center; color: ${!isFlagged ? 'var(--pf-accent)' : '#B45309'}">${scoreDisplay}</td>
          <td style="text-align: center; width: 200px; min-width: 200px;">
            ${statusHtml}
          </td>
          <td style="text-align: right;">
            ${actionBtn}
          </td>
        `;

        tr.querySelector('.student-name-text').addEventListener('click', () => {
          activeStudent = s;
          switchView('student-profile', s);
        });

        const actionEl = tr.querySelector('.btn-table-resolve, .btn-table-review');
        if (actionEl) {
          actionEl.addEventListener('click', () => {
            activeStudent = s;
            switchView('workbench');
          });
        }

        dom.dashSubmissionsTbody.appendChild(tr);
      });
    }

    // 2. Toppers Leaderboard
    dom.dashToppersList.innerHTML = '';
    TOPPERS_LEADERBOARD.forEach((t) => {
      const card = document.createElement('div');
      card.className = `pf-topper-row rank-${t.rank}`;
      card.innerHTML = `
        <div class="pf-topper-left">
          <div class="pf-rank-num font-mono">${t.rank}</div>
          <div class="pf-topper-meta">
            <h4>${t.name} <span class="font-mono text-xs text-muted">(${t.roll})</span></h4>
            <div class="pf-topper-tag">${t.tag}</div>
          </div>
        </div>
        <div class="pf-topper-score">
          <div class="pf-topper-score-val font-mono">${t.score}</div>
          <div class="pf-topper-pct font-mono">${t.pct}</div>
        </div>
      `;

      card.addEventListener('click', () => {
        const found = STUDENTS_DATA.find((s) => s.id === t.studentId);
        if (found) activeStudent = found;
        switchView('workbench');
      });

      dom.dashToppersList.appendChild(card);
    });
  }

  // ==========================================================================
  // 8. MASTER STUDENT DIRECTORY & CANDIDATE DOSSIER
  // ==========================================================================
  function showStudentDirectory() {
    if (dom.studentDirectoryContainer) dom.studentDirectoryContainer.style.display = 'block';
    if (dom.studentDetailContainer) dom.studentDetailContainer.style.display = 'none';
    renderMasterDirectory();
  }

  function showStudentDetail(student) {
    if (student) activeStudent = student;
    if (dom.studentDirectoryContainer) dom.studentDirectoryContainer.style.display = 'none';
    if (dom.studentDetailContainer) dom.studentDetailContainer.style.display = 'block';
    renderStudentProfile(activeStudent);
  }

  function renderMasterDirectory() {
    if (!dom.masterStudentsTbody) return;

    const query = dom.dirStudentSearch ? dom.dirStudentSearch.value.trim().toLowerCase() : '';
    const regionVal = dom.dirFilterRegion ? dom.dirFilterRegion.value : 'ALL';
    const statusVal = dom.dirFilterStatus ? dom.dirFilterStatus.value : 'ALL';

    const filtered = STUDENTS_DATA.filter((s) => {
      // Search query (Candidate name, roll number, registration number, or center)
      if (query) {
        const matchName = s.name.toLowerCase().includes(query);
        const matchRoll = s.rollNo.toLowerCase().includes(query);
        const matchReg = (s.regNo || '').toLowerCase().includes(query);
        const matchCenter = s.center.toLowerCase().includes(query);
        if (!matchName && !matchRoll && !matchReg && !matchCenter) return false;
      }

      // Region filter
      if (regionVal !== 'ALL' && s.region !== regionVal) {
        return false;
      }

      // Status filter
      if (statusVal !== 'ALL') {
        const test = s.tests.find(t => t.id === 'law1') || s.tests[0];
        if (!test || test.status !== statusVal) return false;
      }

      return true;
    });

    if (dom.masterStudentCount) {
      dom.masterStudentCount.textContent = `${filtered.length} of ${STUDENTS_DATA.length} Candidates`;
    }

    dom.masterStudentsTbody.innerHTML = '';

    if (filtered.length === 0) {
      dom.masterStudentsTbody.innerHTML = `
        <tr>
          <td colspan="8" style="text-align: center; padding: 40px 16px; color: var(--pf-muted);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 12px; background: rgba(37, 99, 235, 0.06); border: 1px solid rgba(37, 99, 235, 0.15); margin-bottom: 10px; color: var(--pf-accent);">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
              </svg>
            </div>
            <div style="font-weight: 700; color: var(--pf-ink); font-size: 14px;">No candidates match the selected filters</div>
            <div style="font-size: 11.5px; margin-top: 4px; color: var(--pf-muted);">
              Try resetting your region/status filter or clear the search keyword.
            </div>
          </td>
        </tr>
      `;
      return;
    }

    filtered.forEach((s) => {
      const test = s.tests.find(t => t.id === 'law1') || s.tests[0];
      const isEval = test && test.status === 'Evaluated';
      const statusClass = isEval ? 'evaluated' : 'pending-review';
      const progressPct = isEval ? 100 : 50;

      const displayName = query ? highlightMatch(s.name, query) : s.name;
      const displayRoll = query ? highlightMatch(s.rollNo, query) : s.rollNo;
      const displayReg = query ? highlightMatch(s.regNo || '', query) : (s.regNo || '—');
      const displayCenter = query ? highlightMatch(s.center, query) : s.center;

      const scoreDisplay = test && test.awardedMarks !== null 
        ? `<strong style="color: var(--pf-accent);">${test.awardedMarks.toFixed(1)}</strong> <span class="text-muted">/ ${test.maxMarks.toFixed(1)}</span>`
        : `<span class="text-muted">In Queue</span>`;

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>
          <div class="student-col-info">
            <div class="student-table-avatar">${s.name.split(' ').map(n => n[0]).join('')}</div>
            <div>
              <div class="student-name-text" style="font-weight: 600; color: var(--pf-ink); cursor: pointer;">${displayName}</div>
              <div class="student-roll-tag font-mono">Roll: ${displayRoll} • Reg: ${displayReg}</div>
            </div>
          </div>
        </td>
        <td>
          <div style="font-size: 12px; font-weight: 600; color: var(--pf-ink);">${displayCenter}</div>
          <div class="font-mono text-muted text-xs">${s.region || 'Chapter'}</div>
        </td>
        <td>
          <div style="font-size: 12px; font-weight: 500;">Law Paper 4 (1 Test)</div>
          <div class="font-mono text-xs text-muted">May 2026 Batch</div>
        </td>
        <td style="text-align: center;">
          <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
            <div class="pf-prog-track" style="width: 70px;">
              <div class="pf-prog-fill" style="width: ${progressPct}%;"></div>
            </div>
            <span class="font-mono text-xs text-muted">${progressPct}%</span>
          </div>
        </td>
        <td class="font-mono font-bold" style="text-align: center;">
          ${scoreDisplay}
        </td>
        <td class="font-mono font-bold" style="text-align: center; color: var(--pf-accent);">
          #${s.rank} <span class="text-muted" style="font-size: 10px; font-weight: 400;">/ ${s.totalStudents}</span>
        </td>
        <td style="text-align: center; width: 140px; min-width: 140px; white-space: nowrap;">
          ${!isEval || test.flagged
            ? `<span class="pf-telemetry-badge exception" style="white-space: nowrap;"><span class="pf-telemetry-dot exception"></span>Exception Flag</span>`
            : `<span class="pf-telemetry-badge verified" style="white-space: nowrap;"><span class="pf-telemetry-dot verified"></span>AI Certified</span>`}
        </td>
        <td style="text-align: right;">
          <button class="btn-table-review" data-student-id="${s.id}">
            Inspect Dossier &rarr;
          </button>
        </td>
      `;

      tr.querySelector('.student-name-text').addEventListener('click', () => {
        showStudentDetail(s);
      });

      tr.querySelector('.btn-table-review').addEventListener('click', () => {
        showStudentDetail(s);
      });

      dom.masterStudentsTbody.appendChild(tr);
    });
  }

  function exportStudentsCsv() {
    const headers = ['Candidate Name', 'Roll Number', 'Registration No', 'Region', 'Exam Center', 'Cohort', 'Enrolled Test', 'Max Marks', 'Awarded Marks', 'Percentage', 'AI Autonomy Status', 'AI Confidence', 'AI Exception Flag Reason', 'Batch Rank'];
    const rows = STUDENTS_DATA.map((s) => {
      const test = s.tests.find(t => t.id === 'law1') || s.tests[0];
      const maxM = test ? test.maxMarks : 42;
      const awdM = test && test.awardedMarks !== null ? test.awardedMarks : '';
      const pct = test && test.awardedMarks !== null ? `${((test.awardedMarks / maxM) * 100).toFixed(1)}%` : '';
      const aiSt = test && test.flagged ? 'AI Exception Flag' : 'AI Certified';
      const aiConf = s.aiConfidence || '99.2%';
      const flgReas = s.flagReason || 'None (100% Autonomous Pass)';

      return [
        `"${s.name.replace(/"/g, '""')}"`,
        `"${s.rollNo}"`,
        `"${s.regNo || ''}"`,
        `"${s.region || ''}"`,
        `"${s.center.replace(/"/g, '""')}"`,
        `"${s.cohort || 'May 2026 CA Final'}"`,
        `"${test ? test.name.replace(/"/g, '""') : 'Law Test 1'}"`,
        maxM,
        awdM,
        `"${pct}"`,
        `"${aiSt}"`,
        `"${aiConf}"`,
        `"${flgReas.replace(/"/g, '""')}"`,
        `"#${s.rank} of ${s.totalStudents}"`
      ].join(',');
    });

    const csvContent = [headers.join(','), ...rows].join('\r\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'ParallaxFlow_CA_Student_Master_Roster_May2026.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  function renderStudentProfile(student) {
    dom.profName.textContent = student.name;
    dom.profRoll.textContent = `Roll No: ${student.rollNo}`;
    if (dom.profReg) dom.profReg.textContent = `Reg: ${student.regNo || 'WRO-0648291'}`;
    dom.profCenter.textContent = student.center;
    dom.profRank.textContent = `Batch Rank: #${student.rank} / ${student.totalStudents}`;
    dom.profAvatar.textContent = student.name.split(' ').map(n=>n[0]).join('');

    dom.profTestsGrid.innerHTML = '';
    student.tests.forEach((t) => {
      const isEval = t.status === 'Evaluated';
      const card = document.createElement('div');
      card.className = 'pf-test-card';

      const scoreText = t.awardedMarks !== null ? `${t.awardedMarks.toFixed(1)} / ${t.maxMarks.toFixed(1)} Marks` : 'Pending Evaluation';
      const pctText = t.awardedMarks !== null ? `(${((t.awardedMarks / t.maxMarks) * 100).toFixed(1)}%)` : '';

      card.innerHTML = `
        <div class="pf-test-card-top">
          <div>
            <div class="pf-test-title">${t.name}</div>
            <div class="pf-test-sub font-mono">${t.id.toUpperCase()} • May 2026 Batch</div>
          </div>
          <span class="status-chip ${isEval ? 'evaluated' : 'pending-review'}">${t.status}</span>
        </div>

        <div>
          <div class="pf-test-metrics-row">
            <div>
              <div class="pf-bento-card-label">Score Awarded</div>
              <div class="pf-test-score-huge font-mono">${scoreText} <span style="font-size: 11px; font-weight: 500; color: var(--pf-muted);">${pctText}</span></div>
            </div>
            <div style="text-align: right;">
              <div class="pf-bento-card-label">Submitted</div>
              <div class="font-mono text-xs text-muted">${t.submittedAt}</div>
            </div>
          </div>
          <button class="pf-btn-workbench" data-test-id="${t.id}" style="width: 100%;">
            <span>Open Evaluation Workbench &rarr;</span>
          </button>
        </div>
      `;

      card.querySelector('.pf-btn-workbench').addEventListener('click', () => {
        activeTestId = t.id;
        switchView('workbench');
      });

      dom.profTestsGrid.appendChild(card);
    });
  }

  // ==========================================================================
  // 9. WORKBENCH QUESTION & STEP RENDERING (With Presentation Marks!)
  // ==========================================================================
  function renderWorkbenchQuestion(index) {
    const q = LAW_TEST_1_QUESTIONS[index];
    if (!q) return;

    dom.qPagerLabel.textContent = `${q.no} / ${LAW_TEST_1_QUESTIONS.length}`;

    // Render AI Autonomous Exception Banner if candidate was flagged
    if (dom.wbAiFlagContainer) {
      if (activeStudent && activeStudent.flagged) {
        dom.wbAiFlagContainer.innerHTML = `
          <div class="pf-ai-flag-banner">
            <div class="pf-ai-flag-left">
              <div class="pf-ai-flag-icon-box">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
              </div>
              <div>
                <div class="pf-ai-flag-title-row">
                  <h4>AI Autonomous Exception Flag: Administrative Review Required</h4>
                  <span class="pf-ai-flag-conf-pill font-mono">AI Confidence: ${activeStudent.aiConfidence || '78.4%'}</span>
                  <span class="pf-tag-pill font-mono" style="background: rgba(217, 119, 6, 0.15); color: #B45309; border-color: rgba(217, 119, 6, 0.3);">${activeStudent.name} (Roll: ${activeStudent.rollNo})</span>
                </div>
                <p class="pf-ai-flag-desc">
                  <strong>AI Root-Cause:</strong> ${activeStudent.flagDetails || 'Anomaly detected during autonomous evaluation pass.'}
                </p>
                <div style="font-size: 11px; color: #78350F; margin-top: 5px;">
                  <strong>AI Recommended Action:</strong> ${activeStudent.aiRecommendation || 'Administrator review recommended.'}
                </div>
              </div>
            </div>
            <div class="pf-ai-flag-actions">
              <button class="pf-btn-approve-ai" id="btn-approve-ai-flag">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;"><polyline points="20 6 9 17 4 12"></polyline></svg>Clear Exception &amp; Sign Paper
              </button>
            </div>
          </div>
        `;
        const approveBtn = document.getElementById('btn-approve-ai-flag');
        if (approveBtn) {
          approveBtn.addEventListener('click', () => {
            activeStudent.flagged = false;
            activeStudent.aiStatus = 'AI Certified';
            activeStudent.aiConfidence = '99.5%';
            activeStudent.flagReason = null;
            const test = activeStudent.tests.find(t => t.id === 'law1') || activeStudent.tests[0];
            if (test) {
              test.status = 'Evaluated';
              test.flagged = false;
            }
            showToast(`Paper Certified! AI Autonomous Flag cleared for ${activeStudent.name}.`);
            renderWorkbenchQuestion(activeQuestionIndex);
            renderDashboard();
            renderMasterDirectory();
          });
        }
      } else {
        dom.wbAiFlagContainer.innerHTML = '';
      }
    }

    // 1. Render Horizontal Top Ribbon
    renderQuestionRibbon();

    // 2. Render Left Pane Prompt & Student Text
    dom.wbPromptCode.textContent = q.code;
    dom.wbPromptSection.textContent = q.sectionRef.split(',')[0];
    dom.wbPromptMarks.textContent = `${q.maxMarks.toFixed(1)} Marks`;
    dom.wbPromptTitle.textContent = q.title;
    dom.wbPromptText.textContent = q.promptText;

    // Apply semantic highlights to student answer
    const highlightedText = q.studentText
      .replace(/Section 185/g, '<span class="hl-citation">Section 185</span>')
      .replace(/special resolution/g, '<span class="hl-matched">special resolution</span>')
      .replace(/principal business/g, '<span class="hl-matched">principal business</span>')
      .replace(/Section 135/g, '<span class="hl-citation">Section 135</span>')
      .replace(/net profit of ₹ 5 crore/g, '<span class="hl-matched">net profit of ₹ 5 crore</span>')
      .replace(/Section 68/g, '<span class="hl-citation">Section 68</span>')
      .replace(/free reserves/g, '<span class="hl-matched">free reserves</span>')
      .replace(/securities premium/g, '<span class="hl-matched">securities premium</span>');

    dom.wbTranscriptBody.innerHTML = highlightedText;
    dom.wbDiffBody.innerHTML = `<strong>ICAI Model Benchmark Key:</strong>\n\n${q.icaiModelText}`;
    dom.wbScanBody.innerHTML = `<strong>Margin Reference [${q.code}]:</strong>\n\n${q.studentText}`;

    // 3. Render Right Pane Step Cards (Including Layout Presentation Step!)
    const qTotalScore = q.steps.reduce((acc, s) => acc + s.marks, 0);
    dom.wbRubricTitle.textContent = `${q.code} • ${q.title}`;
    dom.wbQscorePill.textContent = `${qTotalScore.toFixed(1)} / ${q.maxMarks.toFixed(1)} Marks`;

    dom.wbStepCardsContainer.innerHTML = '';
    q.steps.forEach((step) => {
      const card = document.createElement('div');
      card.className = `pf-step-card ${step.isPresentation ? 'presentation-step' : ''}`;

      const isDeducted = step.marks < step.maxMarks;
      const aiDecisionText = isDeducted 
        ? (step.isPresentation ? 'Deducted 0.5 marks: Missing mandatory sub-clause statutory citation as per ICAI format.' : `Deducted ${(step.maxMarks - step.marks).toFixed(1)} marks: Semantic check found omission of ${step.tagsMissing && step.tagsMissing.length ? step.tagsMissing.join(', ') : 'benchmark statutory criteria'}.`)
        : `Full credit awarded: Statutory keywords matched ICAI Suggested Answers model with 100% semantic fidelity.`;

      card.innerHTML = `
        <div class="pf-step-top-row">
          <div class="pf-step-title-group">
            <span class="pf-step-no-badge font-mono">S${step.stepNo}</span>
            <span class="pf-step-title-text">${step.title}</span>
          </div>
          <div class="pf-stepper-control">
            <button class="pf-btn-stepper btn-minus" data-step-no="${step.stepNo}" title="Decrease 0.5 marks">-</button>
            <span class="pf-step-score-val font-mono" id="step-val-${step.stepNo}">${step.marks.toFixed(1)} / ${step.maxMarks.toFixed(1)}</span>
            <button class="pf-btn-stepper btn-plus" data-step-no="${step.stepNo}" title="Increase 0.5 marks">+</button>
          </div>
        </div>

        <div class="pf-step-feedback-text">${step.feedback}</div>

        <div class="pf-ai-decision-chip ${isDeducted ? 'flagged-step' : ''}">
          <span class="pf-ai-spark-label">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -1px; margin-right: 3px;"><polyline points="20 6 9 17 4 12"></polyline></svg>ICAI AUDIT CHECK:
          </span>
          <span>${aiDecisionText}</span>
        </div>
      `;

      // Stepper button logic (-0.5 / +0.5)
      card.querySelector('.btn-minus').addEventListener('click', () => {
        if (step.marks >= 0.5) {
          step.marks -= 0.5;
          updateStepScore(step, q);
        }
      });

      card.querySelector('.btn-plus').addEventListener('click', () => {
        if (step.marks + 0.5 <= step.maxMarks) {
          step.marks += 0.5;
          updateStepScore(step, q);
        }
      });

      dom.wbStepCardsContainer.appendChild(card);
    });
  }

  function renderQuestionRibbon() {
    dom.ribbonTrack.innerHTML = '';
    LAW_TEST_1_QUESTIONS.forEach((q, idx) => {
      const btn = document.createElement('button');
      btn.className = `pf-q-pill-btn ${idx === activeQuestionIndex ? 'active' : ''}`;
      btn.innerHTML = `<span class="font-mono font-bold">${q.code}</span>`;
      btn.title = `${q.title} (${q.maxMarks.toFixed(1)} Marks)`;
      btn.addEventListener('click', () => {
        activeQuestionIndex = idx;
        renderWorkbenchQuestion(activeQuestionIndex);
      });
      dom.ribbonTrack.appendChild(btn);
    });
  }

  function updateStepScore(step, q) {
    const stepValDisplay = document.getElementById(`step-val-${step.stepNo}`);
    if (stepValDisplay) {
      stepValDisplay.textContent = `${step.marks.toFixed(1)} / ${step.maxMarks.toFixed(1)}`;
    }

    const qTotal = q.steps.reduce((acc, s) => acc + s.marks, 0);
    dom.wbQscorePill.textContent = `${qTotal.toFixed(1)} / ${q.maxMarks.toFixed(1)} Marks`;

    renderQuestionRibbon();
    recalculateBatchTotal();
  }

  function recalculateBatchTotal() {
    let grandTotal = 0;
    LAW_TEST_1_QUESTIONS.forEach((q) => {
      grandTotal += q.steps.reduce((acc, s) => acc + s.marks, 0);
    });

    // Update active student test score
    const studentTest = activeStudent.tests.find((t) => t.id === 'law1');
    if (studentTest) {
      studentTest.awardedMarks = grandTotal;
    }

    renderReport();
  }

  function updateCenterModeDisplay() {
    dom.wbOcrCard.style.display = activeMode === 'ocr' ? 'block' : 'none';
    dom.wbDiffCard.style.display = activeMode === 'diff' ? 'block' : 'none';
    dom.wbScanCard.style.display = activeMode === 'scan' ? 'block' : 'none';
  }

  // ==========================================================================
  // 10. GAZETTE REPORT RENDERING
  // ==========================================================================
  function renderReport() {
    let grandTotal = 0;
    let grandMax = 0;
    let provisionMarks = 0;
    let provisionMax = 0;
    let analysisMarks = 0;
    let analysisMax = 0;
    let structureMarks = 0;
    let structureMax = 0;
    let layoutMarks = 0;
    let layoutMax = 0;

    LAW_TEST_1_QUESTIONS.forEach((q) => {
      grandMax += q.maxMarks;
      q.steps.forEach((s) => {
        grandTotal += s.marks;
        if (s.isPresentation) {
          layoutMarks += s.marks;
          layoutMax += s.maxMarks;
        } else if (s.stepNo === 1) {
          provisionMarks += s.marks;
          provisionMax += s.maxMarks;
        } else if (s.stepNo === 2) {
          analysisMarks += s.marks;
          analysisMax += s.maxMarks;
        } else {
          structureMarks += s.marks;
          structureMax += s.maxMarks;
        }
      });
    });

    dom.repName.textContent = activeStudent.name;
    dom.repRoll.textContent = activeStudent.rollNo;
    dom.repScoreHuge.innerHTML = `${grandTotal.toFixed(1)} <span style="font-size: 18px; font-weight: 500; color: var(--pf-muted);">/ ${grandMax.toFixed(1)}</span>`;

    const pct = ((grandTotal / grandMax) * 100).toFixed(1);
    const gradeBadge = document.getElementById('rep-grade-badge');
    if (gradeBadge) {
      gradeBadge.innerHTML = `<span class="status-chip evaluated font-mono">${pct}% • Qualified with Distinction</span>`;
    }

    // 1. Render 4 Core Competency Cards
    const compGrid = document.getElementById('rep-competencies-grid');
    if (compGrid) {
      const provPct = Math.min(100, Math.round((provisionMarks / (provisionMax || 1)) * 100));
      const anaPct = Math.min(100, Math.round((analysisMarks / (analysisMax || 1)) * 100));
      const structPct = Math.min(100, Math.round((structureMarks / (structureMax || 1)) * 100));
      const layPct = Math.min(100, Math.round((layoutMarks / (layoutMax || 1)) * 100));

      compGrid.innerHTML = `
        <div class="pf-rep-comp-card">
          <div class="pf-rep-comp-header">
            <span class="pf-rep-comp-title">Statutory Precision</span>
            <span class="pf-rep-comp-pct">${provPct}%</span>
          </div>
          <div class="pf-rep-comp-bar-bg">
            <div class="pf-rep-comp-bar-fill" style="width: ${provPct}%; background: linear-gradient(90deg, #2563EB, #3B82F6);"></div>
          </div>
          <div class="pf-rep-comp-note">Bare Act citations (§185, §186, §2(6)) consistently accurate. Minor penal clause omission.</div>
        </div>

        <div class="pf-rep-comp-card">
          <div class="pf-rep-comp-header">
            <span class="pf-rep-comp-title">Fact Synthesis</span>
            <span class="pf-rep-comp-pct">${anaPct}%</span>
          </div>
          <div class="pf-rep-comp-bar-bg">
            <div class="pf-rep-comp-bar-fill" style="width: ${anaPct}%; background: linear-gradient(90deg, #0284C7, #38BDF8);"></div>
          </div>
          <div class="pf-rep-comp-note">Strong alignment between problem facts and legal restrictions. Logical deduction well-maintained.</div>
        </div>

        <div class="pf-rep-comp-card">
          <div class="pf-rep-comp-header">
            <span class="pf-rep-comp-title">3-Tier Structure</span>
            <span class="pf-rep-comp-pct">${structPct}%</span>
          </div>
          <div class="pf-rep-comp-bar-bg">
            <div class="pf-rep-comp-bar-fill" style="width: ${structPct}%; background: linear-gradient(90deg, #059669, #10B981);"></div>
          </div>
          <div class="pf-rep-comp-note">Follows ICAI prescribed format: Applicable Law -&gt; Facts Analysis -&gt; Specific Final Advice.</div>
        </div>

        <div class="pf-rep-comp-card">
          <div class="pf-rep-comp-header">
            <span class="pf-rep-comp-title">Layout &amp; Underlining</span>
            <span class="pf-rep-comp-pct">${layPct}%</span>
          </div>
          <div class="pf-rep-comp-bar-bg">
            <div class="pf-rep-comp-bar-fill" style="width: ${layPct}%; background: linear-gradient(90deg, #D97706, #F59E0B);"></div>
          </div>
          <div class="pf-rep-comp-note">Keyword underlining and working note numbering omitted in 3 questions. Potential +3 marks gain.</div>
        </div>
      `;
    }

    // 2. Render Strengths vs. Deductions Grid
    const insightsGrid = document.getElementById('rep-insights-grid');
    if (insightsGrid) {
      insightsGrid.innerHTML = `
        <div class="pf-rep-insight-card strengths">
          <div class="pf-insight-header">
            <span class="pf-insight-icon-box success">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
            </span>
            <h4>Key Scoring Strengths (Preserve for Final Exam)</h4>
          </div>
          <div class="pf-insight-list">
            <div class="pf-insight-item">
              <span class="pf-insight-bullet success"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
              <div><strong>Clear 3-Tier Structuring:</strong> Answer scripts cleanly separate Relevant Legal Provisions, Case Analysis, and Concluding Decision.</div>
            </div>
            <div class="pf-insight-item">
              <span class="pf-insight-bullet success"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
              <div><strong>High Bare Act Precision:</strong> Exact sections cited for Associate Company (§2(6)), Small Company (§2(85)), and Loans to Directors (§185).</div>
            </div>
            <div class="pf-insight-item">
              <span class="pf-insight-bullet success"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
              <div><strong>Exemption Criteria Grasp:</strong> Correctly analyzed Special Resolution requirements and business purpose exceptions under Section 185(2).</div>
            </div>
          </div>
        </div>

        <div class="pf-rep-insight-card deductions">
          <div class="pf-insight-header">
            <span class="pf-insight-icon-box alert">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
            </span>
            <h4>Critical Mark Deductions &amp; Remedial Guidance</h4>
          </div>
          <div class="pf-insight-list">
            <div class="pf-insight-item">
              <span class="pf-insight-bullet deduction"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></span>
              <div><strong>Q.1 (-0.5 Marks): Missing Penal Provision:</strong> Concluded loan was invalid, but omitted Section 185(4) fine (₹5L–₹25L) and officer imprisonment. Always cite penal provisions in non-compliance questions.</div>
            </div>
            <div class="pf-insight-item">
              <span class="pf-insight-bullet deduction"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></span>
              <div><strong>Q.4 (-1.0 Marks): CARO 2020 Clause Reference:</strong> Quoted CARO 2020 generally without specifying Clause 3(i)(c) for title deeds of immovable properties held in company name.</div>
            </div>
            <div class="pf-insight-item">
              <span class="pf-insight-bullet deduction"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></span>
              <div><strong>Q.7 (-0.5 Marks): Statutory Time Periods:</strong> Stated 30 days instead of 60 days for sectoral regulator representations under Section 230(5).</div>
            </div>
            <div class="pf-insight-item">
              <span class="pf-insight-bullet deduction"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></span>
              <div><strong>Layout Polish (-1.0 Marks):</strong> Underline key terms ("Special Resolution", "Ordinary Course of Business") so the examiner spots keywords in 5 seconds.</div>
            </div>
          </div>
        </div>
      `;
    }

    // 3. Render Mentor Directive Card
    const mentorCard = document.getElementById('rep-mentor-card');
    if (mentorCard) {
      mentorCard.innerHTML = `
        <div class="pf-mentor-directive-card">
          <div class="pf-mentor-avatar font-mono" style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: #FFFFFF; font-weight: 800; font-size: 11px; letter-spacing: 0.05em; border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 4px 12px rgba(15, 23, 42, 0.25);">ICAI</div>
          <div class="pf-mentor-content">
            <h4>Autonomous AI Evaluation &amp; Strategic Performance Directive</h4>
            <p class="pf-mentor-quote">
              "${activeStudent.name}, your conceptual understanding of Corporate Law is top-tier. In ICAI subjective papers, candidates who secure rank-level marks differentiate themselves through layout presentation reflexes: insert a dedicated 2-line 'Penal Consequences &amp; Default Liability' heading whenever a company breaches statutory limits, and underline operative legal conditions. Adopt this habit to secure a rank-level 38+/42 in the main exam."
            </p>
            <div class="pf-mentor-sign font-mono">
              — Parallax Flow Autonomous Neural Evaluator v4.2 • Verified against ICAI Suggested Answers May 2026
            </div>
          </div>
        </div>
      `;
    }

    // 4. Executive Table
    dom.repExecTbody.innerHTML = '';
    LAW_TEST_1_QUESTIONS.forEach((q) => {
      const qScore = q.steps.reduce((acc, s) => acc + s.marks, 0);
      const ratio = (qScore / q.maxMarks) * 100;
      const perfLabel = ratio === 100 ? '100% Full Credit' : `${ratio.toFixed(0)}% Partial`;

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="font-mono font-bold">${q.code}</td>
        <td>
          <div class="font-semibold">${q.title}</div>
          <div class="font-mono text-xs text-muted">${q.sectionRef}</div>
        </td>
        <td class="font-mono" style="text-align: center;">${q.maxMarks.toFixed(1)}</td>
        <td class="font-mono font-bold" style="text-align: center; color: var(--pf-accent);">${qScore.toFixed(1)}</td>
        <td style="text-align: center;">
          <span class="status-chip evaluated font-mono">${perfLabel}</span>
        </td>
      `;
      dom.repExecTbody.appendChild(tr);
    });

    // 5. In-Depth Question Audit Trail with Candidate vs ICAI Benchmark Comparison
    dom.repQuestionsAuditTrail.innerHTML = '';
    LAW_TEST_1_QUESTIONS.forEach((q) => {
      const qScore = q.steps.reduce((acc, s) => acc + s.marks, 0);
      const block = document.createElement('div');
      block.className = 'pf-rep-q-block';

      const stepsRows = q.steps.map(s => `
        <tr>
          <td class="font-mono font-bold" style="width: 50px;">S${s.stepNo}</td>
          <td>
            <strong>${s.title}</strong>
            <div style="font-size: 11px; color: var(--pf-muted); margin-top: 2px;">${s.feedback}</div>
          </td>
          <td class="font-mono" style="text-align: center; width: 65px;">${s.maxMarks.toFixed(1)}</td>
          <td class="font-mono font-bold" style="text-align: center; width: 65px; color: var(--pf-accent);">${s.marks.toFixed(1)}</td>
        </tr>
      `).join('');

      block.innerHTML = `
        <div class="pf-rep-q-top">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span class="pf-code-badge">${q.code}</span>
            <strong style="font-size: 13.5px;">${q.title}</strong>
            <span class="pf-section-badge">${q.sectionRef}</span>
          </div>
          <div class="font-mono font-bold" style="font-size: 13px; color: var(--pf-accent);">
            Awarded: ${qScore.toFixed(1)} / ${q.maxMarks.toFixed(1)} Marks
          </div>
        </div>

        <p style="font-size: 11.5px; color: var(--pf-muted); margin: 6px 0 10px; line-height: 1.4;">
          <strong>Question Statement:</strong> ${q.promptText}
        </p>

        <!-- Candidate vs ICAI Solution Comparison -->
        <div class="pf-rep-compare-grid">
          <div class="pf-rep-compare-col">
            <div class="pf-rep-compare-label">
              <span>Candidate Submitted Answer (OCR Extract)</span>
              <span class="font-mono" style="font-size: 9.5px; color: var(--pf-accent);">OCR 99.4%</span>
            </div>
            <div class="pf-rep-compare-text">${q.studentText}</div>
          </div>
          <div class="pf-rep-compare-col" style="background: rgba(240, 248, 255, 0.5); border-color: rgba(186, 218, 255, 0.8);">
            <div class="pf-rep-compare-label" style="color: var(--pf-accent);">
              <span>ICAI Suggested Benchmark Solution</span>
              <span class="font-mono" style="font-size: 9.5px;">Model Key</span>
            </div>
            <div class="pf-rep-compare-text">${q.icaiModelText}</div>
          </div>
        </div>

        <!-- Rubric Step-by-Step Scoring Table -->
        <table class="pf-table" style="background: #FFFFFF; border: 1px solid var(--pf-line-light); border-radius: 10px; overflow: hidden; margin-top: 10px;">
          <thead>
            <tr>
              <th style="width: 50px;">Step</th>
              <th>Evaluated Statutory &amp; Layout Parameter</th>
              <th style="text-align: center; width: 65px;">Max</th>
              <th style="text-align: center; width: 65px;">Marks</th>
            </tr>
          </thead>
          <tbody>
            ${stepsRows}
          </tbody>
        </table>
      `;

      dom.repQuestionsAuditTrail.appendChild(block);
    });
  }

  // Run on page load
  document.addEventListener('DOMContentLoaded', init);
})();
