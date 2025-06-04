import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckCircle, faSearch } from '@fortawesome/free-solid-svg-icons';

const AboutWWSPage = () => {
    useEffect(() => {
        document.title = 'About WWS - RentRightNL';
    }, []);

    const contentSections = [
        {
            title: "What is the Woningwaarderingsstelsel (WWS)?",
            paragraphs: [
                "The Woningwaarderingsstelsel (WWS), often called the \"rent points system,\" is a legal framework in the Netherlands designed to determine the maximum permissible rent for most rental properties. Its primary goal is to protect tenants from excessive rental prices and ensure a fair housing market, particularly in the regulated (social) housing sector.",
                "By assigning points to various aspects of a property, the WWS provides an objective measure of its quality and amenities, which then translates into a maximum legal rent."
            ]
        },
        {
            title: "How are WWS Points Calculated?",
            paragraphs: ["WWS points are awarded based on a detailed evaluation of the property's characteristics. Key factors include:"],
            listItems: [
                "<strong>Surface Area (m&sup2;):</strong> The size of individual rooms and the total living space.",
                "<strong>Energy Efficiency:</strong> The property's energy label (e.g., A++, A, B, C). A better label means more points.",
                "<strong>Kitchen and Bathroom Quality:</strong> The standard of fixtures, fittings, and appliances.",
                "<strong>WOZ-value (Property Value):</strong> The official property valuation by the municipality, which reflects the location and market value.",
                "<strong>Outdoor Spaces:</strong> Presence and size of balconies, gardens, or terraces.",
                "<strong>Shared Spaces & Amenities:</strong> For apartment complexes, common areas and facilities can contribute points.",
                "<strong>Nuisance:</strong> Points can be deducted for significant nuisances like noise pollution."
            ],
            concludingParagraph: "Each feature receives a specific number of points according to official tables. The sum of these points determines the property's total WWS score, which corresponds to a maximum monthly rent."
        },
        {
            title: "Regulated vs. Liberalized Rentals",
            paragraphs: [
                "The WWS is most critical for properties in the <strong>regulated sector</strong>. As of 2024, if a self-contained dwelling has <strong>135 points or fewer</strong> at the start of the tenancy, it generally falls under the regulated sector. The maximum rent calculated via WWS is legally binding. Landlords cannot charge more.",
                "If a property scores <strong>136 points or more</strong> (the \"liberalization threshold\" for 2024, this may change annually), it typically falls into the <strong>liberalized (free) sector</strong>. In this sector, landlords and tenants have more freedom to agree on the rent price. However, even for liberalized properties, the WWS score provides a valuable benchmark for negotiation and understanding the property's intrinsic value.",
                "It's important to note that the initial rent price at the start of the contract is crucial. If it's above the liberalization rent threshold (e.g., &#8364;879.66 in 2024 for properties liberalized based on points), then the contract is usually considered liberalized, even if the points are slightly lower, provided the initial rent was agreed upon fairly."
            ]
        },
        {
            title: "Why is WWS Transparency Important?",
            paragraphs: ["Transparency in WWS scoring empowers tenants by:"],
            listItems: [
                "Allowing them to verify if the asked rent is fair and legal.",
                "Providing a basis for negotiating rent, especially if it seems too high.",
                "Helping to prevent overcharging and exploitation in a competitive housing market.",
                "Contributing to a fairer and more transparent rental market for everyone."
            ],
            concludingParagraph: "Understanding the WWS score gives you confidence and knowledge when searching for your next home."
        },
        {
            title: "Our Commitment at RentRightNL",
            paragraphs: [
                "At RentRightNL, we believe that every renter deserves clarity and fairness. That's why we integrate the WWS points and calculated maximum legal rent directly into our listings. Our goal is to provide you with all the necessary information upfront, so you can make informed decisions and navigate the Dutch rental market with confidence.",
                "We strive to make the complex simple, transforming your rental search from a source of anxiety into an empowering experience. While this platform is a prototype for design demonstration, our vision is a future where such transparency is standard."
            ]
        }
    ];

    return (
        <main className="about-wws-section py-12 bg-white-color">
            <div className="container max-w-3xl mx-auto px-4">
                <h1 className="font-secondary text-3xl md:text-4xl font-bold text-primary text-center mb-10">Understanding the Dutch Rent Points System (WWS)</h1>
                
                {contentSections.map((section, index) => (
                    <div key={index} className="content-block bg-white-color p-6 md:p-8 rounded-lg shadow-md mb-8 border border-border-color">
                        <h2 className="font-secondary text-2xl font-semibold text-text-dark mb-4 pb-2 border-b-2 border-primary inline-block">
                            {section.title}
                        </h2>
                        {section.paragraphs && section.paragraphs.map((p, pIndex) => (
                            <p key={pIndex} className="text-base text-text-dark mb-4 leading-relaxed" dangerouslySetInnerHTML={{ __html: p }} />
                        ))}
                        {section.listItems && (
                            <ul className="list-none p-0 mb-4">
                                {section.listItems.map((item, itemIndex) => (
                                    <li key={itemIndex} className="relative pl-8 mb-2 text-base text-text-dark leading-relaxed">
                                        <FontAwesomeIcon icon={faCheckCircle} className="text-accent absolute left-0 top-1" />
                                        <span dangerouslySetInnerHTML={{ __html: item }} />
                                    </li>
                                ))}
                            </ul>
                        )}
                        {section.concludingParagraph && (
                            <p className="text-base text-text-dark mb-4 leading-relaxed" dangerouslySetInnerHTML={{ __html: section.concludingParagraph }} />
                        )}
                    </div>
                ))}

                <div className="call-to-action text-center mt-8">
                    <Link to="/" className="cta-button inline-flex items-center bg-accent text-white-color py-3 px-6 rounded-md text-lg font-semibold transition-colors duration-300 hover:bg-green-700">
                        <FontAwesomeIcon icon={faSearch} className="mr-2" /> Start Your Transparent Search
                    </Link>
                </div>
            </div>
        </main>
    );
};

export default AboutWWSPage;
