import pytest
from hearings_lib.transcript_parser import Parser


class TestStandardSpeakerPattern:
    LINES = """
    room 2128, Rayburn House Office Building, Hon. Paul E. 
    Kanjorski [chairman of the subcommittee] presiding.
        Members present: Representatives Kanjorski, Sherman, 
    Perlmutter, Foster; Garrett, Royce, and Campbell.
        Chairman Kanjorski. This hearing of the Subcommittee on 
    Capital Markets, Insurance, and Government Sponsored 
    Enterprises will come to order.
        Pursuant to committee rules, each side will have 15 minutes 
    for opening statements. Without objection, all members' opening 
    statements will be made a part of the record.
        I yield myself 5 minutes.
        Good morning. Since the start of the financial crisis, we 
    have done much work to understand its root causes and to pass 
    robust reform legislation, initially in the House, and 
    yesterday in the Senate, that will end the era of ``too-big-to-
    fail'' financial companies; reform credit rating agency 
    operations and regulations; and implement a broad array of 
    sorely-needed measures that will better protect innocent Main 
    Street investors from unscrupulous Wall Street operators.
        In debating these matters, accounting and auditing issues 
    have surfaced more than once. As a result, the House-passed 
    Wall Street Reform bill includes my reforms aimed at responding 
    to the Madoff fraud by better regulating the auditors for 
    broker-dealers. This legislation also contains my provisions 
    designed to enhance the ability of security authorities to 
    coordinate foreign and domestic investigations and to improve 
    the ability of the Public Company Accounting Oversight Board to 
    collect from and share information with foreign entities.
        The bill additionally includes a provision by Congressman 
    Lee of New York providing for an annual accounting transparency 
    hearing, like the one we are having today.
        It further incorporates a provision by Congressman Miller 
    of California to create a financial reporting forum for 
    regulators.
        Finally, Congressman Adler and Capital Market's Ranking 
    Member Garrett, both of New Jersey, amended the bill to exempt 
    small public companies from the Sarbanes-Oxley Act's 
    requirements for external audits of international control, a 
    provision which continues to concern me.
        At today's hearing, we will doubtlessly re-examine each of 
    these matters as well as the pending Supreme Court case on the 
    process for appointing members of the Public Company Accounting 
    Oversight Board. We will also continue to explore whether or 
    not accounting and auditing standards helped to contribute to 
    the financial crisis. Decisions to move problematic assets off 
    of their balance sheets allowed some companies to hide the real 
    nature of their financial health. Moreover, the recent court-
    appointed examiner's report of the Lehman Brothers' bankruptcy 
    highlighted the troubling Repo 105 practice that some companies 
    may use to embellish their financial viability and inaccurately 
    portray leverage. These practices, motivated purely by short-
    term self-interest, are not literary works to be admired; 
    rather, they are fictional stories based on half truths that 
    have no place in our capital markets.
        Accounting standards and those that apply them ought to 
    portray a company's financial condition candidly and in a way 
    that investors can readily understand. Today, we will also 
    explore what progress regulators and standard setters have made 
    to simplify our reporting framework and produce books that 
    investors want to read.
        We will further examine how to improve accounting 
    transparency, decrease regulatory burdens, and address old 
    issues, like auditor concentration, and newer ones, like 
    converging accounting rules.
        The financial crisis demonstrated just how interconnected 
    our economic fortunes are. Capital now moves across 
    international borders at lightning speed, as investors 
    diversify their portfolios and take advantage of opportunities 
    both here and abroad. Investors, therefore, need to have access 
    to timely, accurate financial information that allows them to 
    make apples-to-apples instead of apples-to-oranges comparisons 
    at similar companies around the world.
        While we have moved quickly on converging global accounting 
    standards, we must also proceed carefully to ensure that these 
    rules produce high-quality results for investors. America's 
    markets and its financial reporting framework are among the 
    most developed in the world because of the independence of 
    standard setting and enforcement. To protect the credibility of 
    our markets and to instill investor trust, we must ensure that 
    any new international system continues to adhere to the core 
    principles of independence, transparency, and accuracy.
        In closing, I look forward to hearing from today's 
    witnesses on the state of accounting and auditing regulations, 
    the progress they have each made in improving standards and 
    enforcement, their priorities, their coordination efforts, and 
    the challenges they now or may soon face. I thank each of them 
    for coming and look forward to their testimony.
        I now recognize the gentleman from New Jersey, the ranking 
    member, Mr. Garrett, for 5 minutes.
        Mr. Garrett. I thank the chairman for this important 
    oversight hearing today.
        Thank you to all the witnesses who are here today.
        With all the changes occurring in our regulatory structure, 
    I look forward to all your testimony, the reason being that 
    accountants and auditors do play a crucial role within our 
    financial markets of ensuring that investors basically have the 
    appropriate and reliable information.
        I would like, though, to begin my comments by mentioning 
    the current case that is before the Supreme Court to determine 
    the constitutionality of the Public Company Accounting 
    Oversight Board, the PCAOB, that was created by the Sarbanes-
    Oxley Act, or SOX.
        Let me be clear, I believe that the PCAOB, as currently 
    established, is unconstitutional. I believe it is in direct 
    violation of the appointments clause. And I believe that when 
    the Supreme Court ruling is delivered, maybe as early as next 
    week, they will agree with me on that point.
        Several Congresses ago, I started a caucus in the House 
    called the Constitution Caucus, and one of the goals of that 
    caucus is to educate other Members of Congress about the 
    constitutional limitations on congressional actions in 
    legislation. Too many times, Members of this body simply 
    abdicate their responsibility to examine each law and determine 
    whether it adheres to the Constitution or not.
        Our Founding Fathers expressly stated that it is incumbent 
    on all three branches of government, not just the Judiciary, to 
    examine and determine the constitutionality of each law before 
    them. So no Member of Congress should ever pass legislation and 
    say, we will just let the courts decide if this is 
    constitutional or not. Each Member must look at each law and 
    determine for themselves if the legislation is within the 
    confines of the Constitution. Maybe if more Members had done 
    this, for example, with the health care bill, we wouldn't have 
    passed a basically unconstitutional monstrosity like the House 
    and Senate did.
        So, partly in response to my concerns on the 
    constitutionality of PCAOB, I introduced legislation 3 years 
    ago, we called it the Amend Misinterpreted Excessive Regulation 
    in Corporate America Act, which basically came out to be the 
    AMERICA Act. And one provision in the AMERICA Act just simply 
    attempted to fix the appointment clause at the heart of the 
    current Supreme Court case by requiring that the PCAOB, the 
    Board, be appointed directly by the President and confirmed by 
    the Senate. If you think about it, had more of my colleagues 
    focused on this issue then, perhaps we would not have had to 
    engage in this very long and drawn out and also costly legal 
    battle that is going on across the street.
        And when you consider the constitutionality of the PCAOB, 
    it has been given question for a number of years, I am not sure 
    why we are giving this same body additional powers and 
    authorities until this is determined. We marked up legislation 
    affecting the PCAOB in November of 2009, and less than a month 
    later, the Supreme Court was hearing arguments as to whether or 
    not the entity should even exist.
        I believe it is prudent before Congress gives different 
    entities more powers, that we make sure that those entities are 
    operating in a manner in accord with the Constitution.
        Now, another issue from the Sarbanes-Oxley law currently 
    being debated as part of the financial regulatory reform 
    package is whether to permanently exempt small businesses from 
    the costly independent auditor attestation of management 
    internal controls. Now, I know my good friend here, Chairman 
    Kanjorski, and I differ on this topic, but during this economic 
    downturn, where thousands of small businesses across the 
    country are really struggling just to make payroll, I don't 
    really see how adding one more costly, burdensome regulation--
    which at best has dubious benefits--will help improve the 
    number of jobs in the country or improve the economy.
        And so I will repeat my comments from yesterday by stating 
    that this is one of numerous ways we can help small businesses 
    without creating another TARP program or throwing another $30 
    billion at deficit spending.
        In regards to the Financial Accounting Standards Board, 
    FASB, I look forward to hearing how the changes and additional 
    guidance you have provided to fair accounting so far have 
    worked. I would also like to explore in greater detail with 
    both FASB and the SEC the recent changes to the securitization 
    rules and 166 and 167 and regulation A-B and the potential 
    impact that those new rules, when you combine them and couple 
    them with the new proposals, will basically have on the 
    availability of the cost of credit.
        I am also very interested in learning further on the 
    progress, as some of you have talked about, of international 
    convergence of accounting standards. I believe this is a 
    critical long-term goal for international competitiveness, and 
    I want to make sure that we are moving forward, as I think we 
    will probably hear, on this expeditiously.
        So, again, I want to thank the chairman for holding this 
    oversight hearing. I think general oversight hearings with 
    government regulators are very informative; they allow us as 
    Members to discuss a wide range of issues. We are going to do 
    another such hearing next week with the FHFA, and later on in 
    June with the SEC and Chairman Schapiro. I do look forward to 
    those.
        And once again, I thank the members of the panel before us.
        I yield back.
        Chairman Kanjorski. Thank you very much, Mr. Garrett.
        I will now recognize the gentleman from California, Mr. 
    Sherman, for 5 minutes.
        Mr. Sherman. I thank the chairman for holding these 
    hearings. Due to my flight schedule, I may not be here to the 
    very end, but I recognize the importance of these hearings.
        The chairman comments on the action taken by the Senate. I 
    have been informed that the Senate passed the bill without 
    passing the manager's amendment. If that is true, then section 
    210(n)10 remains a phony limit on the amount that the FDIC can 
    borrow of taxpayer funds in order to help the creditors of 
    defunct financial institutions. I am confident that anyone who 
    voted for the bill in the Senate really intended the manager's 
    amendment to be part of it, and I am confident that those 
    limits, which are so important to the bailout versus nonbailout 
    question, will be dealt with.
        These hearings are on auditing standards and accounting 
    principles. I will leave to others the discussion of the 
    auditing standards and the discussion of section 404, because 
    accounting principles are so important.
        Corporations dedicate their focus to showing higher 
    earnings per share. He who controls the rules controls the 
    behavior of corporate America. The FASB, therefore, has the 
    highest ratio of anonymity-to-power of any entity in the 
    business world.
        I have been one of the loudest voices in Congress for the 
    independence of the FASB, not because I was convinced they were 
    doing a great job, but because I thought they could do better, 
    and I wasn't so sure that Congress would be helpful. And I was 
    also told again and again, don't worry, international standards 
    are on the way, and they will solve all the problems.
        Mr. Herz, we will get the international standards when you 
    and I get hair.
        And so, we do have to take a look at whether the accounting 
    standards make any sense from an accounting theory standpoint.
        Accounting theory would tell you that two companies should 
    be comparable and that companies that are virtually identical 
    should have identical results, notwithstanding superficial 
    differences, and yet we still have one company to choose LIFO 
    and another company to choose FIFO. Why? Because accounting 
    theory isn't as important as just keeping everybody happy: Let 
    the business world do what they want; investors, figure it out 
    on your own.
        We dealt with some non-optional requirements with stock 
    options, and I think that may have been a step in the right 
    direction. As to mark-to-market, these much ballyhooed rules 
    don't really give you comparability, because if one bank 
    invests in a $100 million loan on a shopping center which they 
    hold for their own portfolio, they made the loan the old 
    fashioned way, and another invests in $100 million worth of 
    collateralized debts, collateralized by shopping centers, 
    perhaps identical shopping centers, the two would be treated 
    differently under this rule. And yet, all the shopping centers 
    are down in value, not just the ones where the debt happened to 
    be securitized.
        But the biggest problem the FASB has is the desire to go 
    with the verifiable rather than the relevant, the desire to 
    make it easy on the auditor rather than useful for the 
    investor. And the best example of this, and by far the most 
    harmful act that nobody ever talks about, is FAS 2, which 
    requires the write-off of all research expenses; penalizes 
    those companies that choose to do research, while we in 
    Congress are providing large benefits to those same companies, 
    and while I think most people agree that the success of America 
    depends upon the research done in the private sector. This 
    isn't good accounting. Good accounting says you are supposed to 
    capitalize research expenditures that provide useful results.
        Why do we have FAS 2? Because good accounting theory would 
    require accountants to distinguish between useful and useless 
    research projects. That is difficult. That is like eliminating 
    the strike zone in baseball and saying every pitch is a strike 
    because the umpires don't want to be second-guessed as to their 
    ball and strike calls. The fact is, for us to be penalizing 
    those corporations that engage in research, making them write 
    off the money they spend, providing higher earnings per share 
    to those companies that choose not to do research, and to do 
    this, not only in the high-tech sector where I think investors 
    may be savvy enough to adjust for it, but in the rest of our 
    economy where research is also important, is the most harmful 
    thing that has been done to our economy that nobody knows 
    about.
        So I look forward to going back to good accounting, when it 
    comes to research, instead of adopting a system that is easy 
    for the umpire and terrible for everyone in the ballpark.
        I yield back.
        Chairman Kanjorski. Thank you very much, Mr. Sherman.
        I now recognize the gentleman from California, Mr. 
    Campbell, for 3 minutes.
    [Whereupon, at 11:50 a.m., the hearing was adjourned.]
    """

    def test_happy_path(self):
        lines = """
        for the umpire and terrible for everyone in the ballpark.
            I yield back.
            Chairman Kanjorski. Thank you very much, Mr. Sherman.
            I now recognize the gentleman from California, Mr. 
        Campbell, for 3 minutes.
        [Whereupon, at 11:50 a.m., the hearing was adjourned.]
        """

        actual = Parser().parse(lines.split('\n'))
        print(actual)
        assert len(actual[0]) == 2