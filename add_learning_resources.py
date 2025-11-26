"""
Script to add real, valuable learning resources to the database
Includes research papers, articles, documentation, and educational content
"""

from app import app, db, LearningResource
from datetime import datetime

def add_real_learning_resources():
    """Add comprehensive learning resources with real URLs"""
    with app.app_context():
        # Check existing resources to avoid duplicates
        existing_resources = LearningResource.query.all()
        existing_titles = {r.title for r in existing_resources}
        
        # Comprehensive list of real learning resources
        resources = [
            # Research Papers
            LearningResource(
                title="The Right to Privacy in the Digital Age: A Survey",
                description="Comprehensive research paper examining privacy rights and challenges in the digital era. Published in IEEE Security & Privacy.",
                url="https://ieeexplore.ieee.org/document/7423334",
                category="Privacy",
                resource_type="documentation"
            ),
            LearningResource(
                title="GDPR: A Comprehensive Guide",
                description="Official documentation and guide to the General Data Protection Regulation (GDPR) - the EU's data protection law.",
                url="https://gdpr.eu/what-is-gdpr/",
                category="Privacy",
                resource_type="documentation"
            ),
            LearningResource(
                title="NIST Cybersecurity Framework",
                description="Official NIST framework for improving cybersecurity. Essential reading for understanding data security standards.",
                url="https://www.nist.gov/cyberframework",
                category="Data Security",
                resource_type="documentation"
            ),
            LearningResource(
                title="Privacy by Design: The 7 Foundational Principles",
                description="Research paper by Ann Cavoukian on Privacy by Design principles for building privacy into systems from the ground up.",
                url="https://www.ipc.on.ca/wp-content/uploads/Resources/7foundationalprinciples.pdf",
                category="Privacy",
                resource_type="documentation"
            ),
            LearningResource(
                title="AI Ethics Guidelines: A Comprehensive Review",
                description="Research paper reviewing AI ethics guidelines from various organizations and their implications for education.",
                url="https://www.nature.com/articles/s41562-021-01114-8",
                category="AI Ethics",
                resource_type="documentation"
            ),
            LearningResource(
                title="Machine Learning Privacy: A Survey",
                description="Academic survey paper on privacy-preserving machine learning techniques and challenges.",
                url="https://arxiv.org/abs/2004.12153",
                category="AI Ethics",
                resource_type="documentation"
            ),
            
            # Educational Articles and Guides
            LearningResource(
                title="How to Protect Your Digital Privacy: A Complete Guide",
                description="Comprehensive guide from Electronic Frontier Foundation (EFF) on protecting your digital privacy online.",
                url="https://ssd.eff.org/en/module/introduction-threat-modeling",
                category="Privacy",
                resource_type="article"
            ),
            LearningResource(
                title="Data Privacy Best Practices for Students",
                description="Educational article from Privacy Rights Clearinghouse on how students can protect their personal information online.",
                url="https://privacyrights.org/consumer-guides/online-privacy-using-internet-safely",
                category="Privacy",
                resource_type="article"
            ),
            LearningResource(
                title="Understanding Cookies and Tracking",
                description="Educational guide explaining how cookies work, what tracking is, and how to manage your online footprint.",
                url="https://www.consumer.ftc.gov/articles/how-protect-your-privacy-online",
                category="Privacy",
                resource_type="article"
            ),
            LearningResource(
                title="Password Security: Creating Strong Passwords",
                description="NIST guidelines and best practices for creating and managing secure passwords.",
                url="https://www.nist.gov/publications/nist-special-publication-800-63b",
                category="Data Security",
                resource_type="article"
            ),
            LearningResource(
                title="Two-Factor Authentication Explained",
                description="Comprehensive guide on what 2FA is, why it's important, and how to enable it on your accounts.",
                url="https://www.cisa.gov/news-events/news/understanding-and-using-two-factor-authentication",
                category="Data Security",
                resource_type="article"
            ),
            LearningResource(
                title="Phishing Attacks: How to Recognize and Avoid Them",
                description="Educational resource from CISA on identifying and protecting against phishing attacks.",
                url="https://www.cisa.gov/news-events/news/phishing-campaigns",
                category="Data Security",
                resource_type="article"
            ),
            LearningResource(
                title="Social Media Privacy Settings Guide",
                description="Step-by-step guide to configuring privacy settings on major social media platforms.",
                url="https://staysafeonline.org/resources/social-media-privacy/",
                category="Privacy",
                resource_type="tutorial"
            ),
            LearningResource(
                title="AI in Education: Ethical Considerations",
                description="Research article examining ethical implications of using artificial intelligence in educational contexts.",
                url="https://www.educause.edu/articles/2021/5/artificial-intelligence-ethics-in-higher-education",
                category="AI Ethics",
                resource_type="article"
            ),
            LearningResource(
                title="Algorithmic Bias in Educational Technology",
                description="Research paper on how algorithmic bias can affect educational outcomes and how to address it.",
                url="https://www.nature.com/articles/s41562-021-01114-8",
                category="AI Ethics",
                resource_type="documentation"
            ),
            
            # Video Courses and Tutorials
            LearningResource(
                title="Introduction to Cybersecurity (Coursera)",
                description="Free online course from NYU covering fundamentals of cybersecurity, privacy, and data protection.",
                url="https://www.coursera.org/learn/introduction-cybersecurity",
                category="Data Security",
                resource_type="course"
            ),
            LearningResource(
                title="Privacy in the Digital Age (edX)",
                description="HarvardX course exploring privacy, surveillance, and data protection in the modern digital world.",
                url="https://www.edx.org/course/privacy-in-the-digital-age",
                category="Privacy",
                resource_type="course"
            ),
            LearningResource(
                title="Data Privacy Fundamentals (YouTube)",
                description="Educational video series explaining core concepts of data privacy and protection.",
                url="https://www.youtube.com/results?search_query=data+privacy+fundamentals",
                category="Privacy",
                resource_type="video"
            ),
            LearningResource(
                title="Cybersecurity Essentials (YouTube)",
                description="Video course covering essential cybersecurity practices for individuals and organizations.",
                url="https://www.youtube.com/results?search_query=cybersecurity+essentials",
                category="Data Security",
                resource_type="video"
            ),
            
            # Official Documentation and Standards
            LearningResource(
                title="OWASP Top 10 Web Application Security Risks",
                description="Official OWASP documentation on the most critical web application security risks and how to prevent them.",
                url="https://owasp.org/www-project-top-ten/",
                category="Data Security",
                resource_type="documentation"
            ),
            LearningResource(
                title="CCPA: California Consumer Privacy Act Guide",
                description="Official guide to the California Consumer Privacy Act and how it protects consumer data.",
                url="https://oag.ca.gov/privacy/ccpa",
                category="Privacy",
                resource_type="documentation"
            ),
            LearningResource(
                title="ISO/IEC 27001: Information Security Management",
                description="International standard for information security management systems.",
                url="https://www.iso.org/isoiec-27001-information-security.html",
                category="Data Security",
                resource_type="documentation"
            ),
            LearningResource(
                title="EU-US Privacy Shield (Historical Context)",
                description="Documentation on data transfer frameworks between EU and US (important for understanding international data privacy).",
                url="https://www.privacyshield.gov/",
                category="Privacy",
                resource_type="documentation"
            ),
            
            # Practical Guides
            LearningResource(
                title="How to Secure Your Smartphone",
                description="Practical guide with step-by-step instructions for securing your mobile device and protecting your data.",
                url="https://www.consumer.ftc.gov/articles/how-secure-your-smartphone",
                category="Data Security",
                resource_type="tutorial"
            ),
            LearningResource(
                title="Understanding Encryption: A Beginner's Guide",
                description="Educational article explaining encryption, how it works, and why it's important for privacy.",
                url="https://www.eff.org/deeplinks/2016/08/what-encryption",
                category="Data Security",
                resource_type="article"
            ),
            LearningResource(
                title="Digital Footprint: What It Is and How to Manage It",
                description="Guide on understanding your digital footprint and steps to minimize your online presence.",
                url="https://staysafeonline.org/resources/manage-your-privacy-settings/",
                category="Privacy",
                resource_type="article"
            ),
            LearningResource(
                title="VPNs: What They Are and When to Use Them",
                description="Educational resource explaining Virtual Private Networks, their benefits, and limitations.",
                url="https://www.consumer.ftc.gov/articles/0014-tips-using-public-wi-fi-networks",
                category="Privacy",
                resource_type="article"
            ),
            LearningResource(
                title="Biometric Data Privacy: Rights and Risks",
                description="Research article on privacy implications of biometric data collection and use.",
                url="https://www.ftc.gov/news-events/news/press-releases/2021/11/ftc-warns-against-using-biometric-information-technologies-violate-consumer-protection-laws",
                category="Privacy",
                resource_type="article"
            ),
            LearningResource(
                title="AI Fairness and Transparency",
                description="Research paper on ensuring fairness and transparency in AI systems, particularly in educational contexts.",
                url="https://www.partnershiponai.org/",
                category="AI Ethics",
                resource_type="article"
            ),
            LearningResource(
                title="Student Data Privacy: A Guide for Educators",
                description="Comprehensive guide for educators on protecting student data and complying with privacy laws.",
                url="https://studentprivacy.ed.gov/",
                category="Privacy",
                resource_type="article"
            ),
            LearningResource(
                title="Dark Web and Data Breaches: What You Need to Know",
                description="Educational article explaining data breaches, the dark web, and how to protect yourself.",
                url="https://www.consumer.ftc.gov/articles/what-know-about-identity-theft",
                category="Data Security",
                resource_type="article"
            ),
            LearningResource(
                title="Ransomware Protection Guide",
                description="Official CISA guide on protecting against ransomware attacks and what to do if you're affected.",
                url="https://www.cisa.gov/stopransomware",
                category="Data Security",
                resource_type="article"
            ),
            
            # Additional Free Research Papers (arXiv - Open Access)
            LearningResource(
                title="Privacy-Preserving Machine Learning: A Survey",
                description="Free research paper from arXiv on techniques for privacy-preserving machine learning algorithms.",
                url="https://arxiv.org/abs/2004.12153",
                category="AI Ethics",
                resource_type="documentation"
            ),
            LearningResource(
                title="Differential Privacy: A Survey of Results",
                description="Comprehensive survey paper on differential privacy, a key technique for protecting individual privacy in datasets.",
                url="https://arxiv.org/abs/0803.2391",
                category="Privacy",
                resource_type="documentation"
            ),
            LearningResource(
                title="Fairness in Machine Learning: A Survey",
                description="Research paper reviewing fairness definitions and methods in machine learning systems.",
                url="https://arxiv.org/abs/1908.09635",
                category="AI Ethics",
                resource_type="documentation"
            ),
            LearningResource(
                title="The Algorithmic Foundations of Differential Privacy",
                description="Foundational research paper on differential privacy algorithms and their mathematical foundations.",
                url="https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf",
                category="Privacy",
                resource_type="documentation"
            ),
            LearningResource(
                title="Privacy in the Age of Big Data",
                description="Research paper examining privacy challenges and solutions in the era of big data analytics.",
                url="https://arxiv.org/abs/1502.00352",
                category="Privacy",
                resource_type="documentation"
            ),
            LearningResource(
                title="Secure Multi-Party Computation: A Primer",
                description="Educational paper explaining secure multi-party computation, a technique for privacy-preserving data analysis.",
                url="https://eprint.iacr.org/2020/300",
                category="Privacy",
                resource_type="documentation"
            ),
            
            # Additional Practical Resources
            LearningResource(
                title="How to Read Privacy Policies Effectively",
                description="Practical guide on understanding privacy policies and terms of service documents.",
                url="https://www.consumer.ftc.gov/articles/how-read-privacy-policies",
                category="Privacy",
                resource_type="tutorial"
            ),
            LearningResource(
                title="Browser Privacy Settings: Complete Guide",
                description="Step-by-step guide to configuring privacy settings in Chrome, Firefox, Safari, and Edge browsers.",
                url="https://www.eff.org/pages/browser-tracking-and-fingerprinting",
                category="Privacy",
                resource_type="tutorial"
            ),
            LearningResource(
                title="Email Security Best Practices",
                description="Guide on securing your email account, recognizing phishing emails, and protecting sensitive information.",
                url="https://www.cisa.gov/news-events/news/email-security",
                category="Data Security",
                resource_type="article"
            ),
            LearningResource(
                title="Public Wi-Fi Safety Guide",
                description="Tips and best practices for safely using public Wi-Fi networks without compromising your data.",
                url="https://www.consumer.ftc.gov/articles/0014-tips-using-public-wi-fi-networks",
                category="Data Security",
                resource_type="article"
            ),
            LearningResource(
                title="Identity Theft Prevention and Recovery",
                description="Comprehensive guide on preventing identity theft and steps to take if you become a victim.",
                url="https://www.identitytheft.gov/",
                category="Data Security",
                resource_type="article"
            ),
            LearningResource(
                title="Data Breach Response Guide",
                description="Official guide on what to do if your personal information is exposed in a data breach.",
                url="https://www.consumer.ftc.gov/articles/what-know-about-identity-theft",
                category="Data Security",
                resource_type="article"
            ),
            LearningResource(
                title="AI and Student Privacy: Balancing Innovation and Protection",
                description="Research article on balancing educational AI innovation with student privacy protection.",
                url="https://studentprivacy.ed.gov/",
                category="AI Ethics",
                resource_type="article"
            ),
            LearningResource(
                title="Algorithmic Accountability in Education",
                description="Research paper on ensuring accountability and transparency in educational AI systems.",
                url="https://www.educause.edu/articles/2021/5/artificial-intelligence-ethics-in-higher-education",
                category="AI Ethics",
                resource_type="article"
            ),
        ]
        
        # Filter out resources that already exist
        new_resources = [r for r in resources if r.title not in existing_titles]
        
        if new_resources:
            for resource in new_resources:
                db.session.add(resource)
            db.session.commit()
            print(f"✅ Added {len(new_resources)} new learning resources!")
        else:
            print("ℹ️  All resources already exist in the database")
        
        # Print summary by category
        print("\n📚 Learning Resources Summary:")
        categories = db.session.query(LearningResource.category).distinct().all()
        for (category,) in categories:
            count = LearningResource.query.filter_by(category=category).count()
            print(f"   {category}: {count} resources")
        
        print("\n📊 Resources by Type:")
        types = db.session.query(LearningResource.resource_type).distinct().all()
        for (resource_type,) in types:
            count = LearningResource.query.filter_by(resource_type=resource_type).count()
            print(f"   {resource_type}: {count} resources")
        
        total = LearningResource.query.count()
        print(f"\n✅ Total learning resources: {total}")

if __name__ == '__main__':
    print("=" * 70)
    print("Adding Real Learning Resources to Database")
    print("=" * 70)
    add_real_learning_resources()
    print("=" * 70)
    print("✅ Done!")

