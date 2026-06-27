# Tawfeer-AlQuaa
AI-powered food waste reduction and donation system for Al Qua'a

# Tawfeer — Reducing Food Waste in Al Qua'a

## 1. Selected Challenge

We selected **Challenge 5 — Free choice, solve a real problem in your community**.

## 2. Specific Problem

In Al Qua'a, food waste can happen in homes, restaurants, supermarkets, farms, institutions, family gatherings, and local events. Some food is still safe and can help people in need, but there is no simple local digital system that organizes donation, food requests, quality control, delivery, reuse, and government monitoring in one place.

At the same time, some families or individuals may need food support because of financial difficulty, job loss, or personal circumstances. Without a clear system, edible food may be wasted while people who need support may not receive help quickly.

## 3. Target Demographic

Tawfeer is designed for the Al Qua'a community, including:

* Homeowners who have extra cooked or uncooked food.
* Restaurants, supermarkets, farms, and institutions that have surplus food.
* Families hosting food feasts and gatherings who often have large amounts of leftover food.
* People or families who need food support.
* Drivers or volunteers who collect and deliver food.
* Administrators who approve requests and manage the workflow.
* Government entities that want to monitor food waste reduction and sustainability results.

## 4. Situation They Face

Food donors may not know where to send extra food, how to make sure it is handled safely, or how to reach people who need it. People in need may not have a simple way to request food while mentioning allergies or special food restrictions. Administrators need a way to review donations and requests before delivery. Drivers need clear tasks and locations. Government entities need a dashboard to track the amount of food saved, reused, donated, and prevented from being wasted.

## 5. Our Solution

**Tawfeer** is a mobile application that helps reduce food waste in Al Qua'a by connecting food donors, people in need, administrators, drivers, and government monitoring in one organized system.

The application allows users to:

* Donate extra food.
* Request food support.
* Reuse leftover or uncooked food using artificial intelligence.
* Track donation status.
* Earn points after successful donation.
* Help reduce food waste in the local community.

## 6. Food Donation Flow

When a user donates food, they fill in important information, including:

* Whether the food is cooked or uncooked.
* Whether the food is safe to eat.
* A description of the donated food.
* A photo of the food.
* Contact phone number.
* Current location.

After submitting the donation, the user waits for administrator approval.

If the donation is accepted and completed, the donor receives reward points. These points can be used to buy discount cards from recognized stores. This encourages people to donate food instead of throwing it away.

## 7. Food Safety and Reuse Flow

Tawfeer separates donated food based on its condition:

### Safe for Human Consumption

If the food is safe to eat, it moves to the quality control stage. The food is checked to make sure it is clean, suitable, and safe before being packaged and delivered to people in need.

### Not Safe for Human Consumption but Suitable for Animals

If the food is not suitable for humans but can still be used safely for animals, it can be redirected to animal feed.

### Not Consumable by Humans or Animals

If the food is not consumable by humans or animals, Tawfeer redirects it to other sustainable uses such as:

* Clean energy production.
* Organic fertilizer.
* Composting.

This means the food is not simply wasted, even when it cannot be eaten.

## 8. Food Request Flow

Users who need food support can submit a food request. The request form includes:

* Reason for the request, such as job loss or financial difficulty.
* Food allergies or restrictions, such as fish, lactose, or other ingredients.
* Contact phone number.
* Current location.

After submitting the request, the user waits for administrator approval. If approved, the administrator assigns a driver to deliver suitable food.

## 9. AI Food Reuse Feature

Tawfeer includes an AI recipe feature that helps users reuse food before it expires.

The user enters:

* The ingredients they already have.
* Whether the food was cooked before or not.
* Any food restrictions if needed.

The AI then provides a step-by-step recipe using the available ingredients. This helps families and individuals reduce waste at home by turning leftover or uncooked food into useful meals.

## 10. System Interfaces

Tawfeer has four main interfaces:

### User Interface

The user interface allows users to donate food, request food, use the AI recipe feature, upload photos, add location, track request status, and collect reward points.

### Administrator Dashboard

The administrator dashboard allows the admin to manage accounts, browse users, delete accounts, accept or reject food donations, accept or reject food requests, assign drivers, and manage the full donation and delivery workflow.

### Driver Interface

The driver interface shows the driver the collection and delivery tasks assigned by the administrator. The driver can view order details, contact the user, share arrival time, and use the location to collect or deliver food accurately.

### Government Dashboard

The government dashboard allows government entities to monitor the impact of Tawfeer in Al Qua'a. It tracks:

* Number of users.
* Number of food donations.
* Number of food requests.
* Amount of food saved from waste.
* Amount of food reused through AI recipes.
* Amount of food delivered to people in need.
* Amount of food redirected to animal feed.
* Amount of food redirected to clean energy.
* Amount of food redirected to organic fertilizer or compost.
* Sustainability indicators and community impact.

This dashboard helps support sustainability goals by showing clear data about how much food was not wasted and how Tawfeer is helping the community.

## 11. Impact with Testable Claims

Tawfeer makes a direct impact on Al Qua'a by reducing food waste, supporting people in need, and encouraging responsible food use.

The impact can be tested using measurable indicators such as:

* Number of completed donations.
* Number of accepted food requests.
* Kilograms of food saved from waste.
* Number of meals delivered to people in need.
* Number of AI recipes generated.
* Number of donations redirected to animal feed, energy, or organic fertilizer.
* Average time from donation approval to driver assignment.
* Number of active donors, recipients, drivers, and institutions.

These indicators can be shown in the admin and government dashboards to prove the value of the solution.

## 12. Feasibility and Deployment

Tawfeer is feasible because it can start as a focused local solution for Al Qua'a before expanding to other areas. The first deployment can use a simple workflow:

1. Users submit donations or requests.
2. Admin reviews and approves them.
3. Admin assigns drivers.
4. Drivers collect and deliver food.
5. The system updates the dashboard.
6. Government users track the results.

The solution does not require expensive hardware at the beginning. It mainly requires a mobile application, database, admin dashboard, driver interface, and government dashboard. It can begin with a small number of local donors, volunteers, and institutions, then grow gradually.

## 13. Scalability Beyond the Event

Tawfeer starts in Al Qua'a, but it can scale to other rural communities in the UAE. The same model can be repeated in other areas by adding new locations, local administrators, drivers, partner stores, restaurants, supermarkets, farms, charities, and government users.

Future improvements can include:

* More accurate AI food classification.
* Integration with food banks and charities.
* Automatic driver route optimization.
* QR code tracking for food packages.
* More detailed sustainability reports.
* More reward partners and discount cards.
* Support for Arabic and English users.

## 14. Tools and Technologies Used

Tawfeer was built using the following technologies:

* **React Native:** Used to build the mobile application interface for users, admins, drivers, and government users.
* **MongoDB:** Used as the database to store users, food donations, food requests, driver tasks, reward points, and dashboard statistics.
* **Python:** Used to build the backend logic and connect the system features together.
* **REST API:** Used to connect the mobile application with the database, admin dashboard, driver interface, government dashboard, and AI recipe feature.
* **ChatGPT-3.5 API:** Used for the AI food reuse feature, where users enter leftover or uncooked ingredients and receive a step-by-step recipe.
* **GitHub:** Used to submit the public repository, including the README, source code, screenshots, documentation, and demo video link.

## 15. Evidence and Validation

The repository includes several files that help validate Tawfeer:

Screenshots of the user interface.
Screenshots of the food donation process.
Screenshots of the food request process.
Screenshots of the AI food reuse feature.
Screenshots of the admin dashboard.
Screenshots of the driver interface.
Screenshots of the government dashboard.
Demo videos showing the project workflow.
Project documentation and business plan.
Source code ZIP file.

These materials show that Tawfeer is not only an idea, but a working prototype with clear features and a complete workflow.

## Demo Video

Watch the Tawfeer demo videos here:  
https://drive.google.com/drive/folders/1qg6kpV0Wjl9HCrtStyTvJB5PGtsUlNpO?usp=sharing

