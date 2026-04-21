# PulsePath

PulsePath is a final-year project prototype designed to improve crowd awareness and movement at festivals and large-scale events.

It combines a live interactive map, real-time crowd updates, and attendee-focused notifications to simulate how both organisers and attendees can make better decisions in busy environments.

This repository is shared as a **codebase showcase** of the project.

---

## Overview

At large events, both organisers and attendees often lack clear visibility of crowd conditions in real time.

PulsePath explores how this gap can be addressed through a browser-based system that:

- visualises crowd density across key zones (e.g. stages)
- updates the interface dynamically as conditions change
- provides simple, actionable signals rather than complex analytics
- supports both organiser monitoring and attendee navigation

---

## Key Features

- Interactive festival map built with **Mapbox GL JS**
- Real-time crowd level indicators (low / medium / high)
- Zone-based tracking using predefined stage boundaries
- Live UI updates powered by WebSockets
- Personal lineup selection for attendees
- Context-aware notifications based on selected artists and crowd conditions
- Organiser dashboard with simulated crowd movement insights
- Mobile-responsive design for usability in live environments

---

## What This Project Demonstrates

This prototype was built to demonstrate:

- real-time communication between backend and frontend
- dynamic UI updates in response to live data
- map-based interaction in a web application
- translating a real-world problem into a working technical solution
- structuring a full-stack Django project with live features

---

## My Contribution

PulsePath was developed as a **two-person final-year project**, and my contribution focused on both user experience and core functionality.

I was responsible for:

- building and refining key frontend pages and flows
- implementing the interactive map interface and UI behaviour
- designing and integrating real-time attendee/organiser notifications
- improving how live crowd data was surfaced through the interface
- contributing to backend integration and debugging during development
- shaping the overall product direction to ensure the prototype was both usable and meaningful

This work went beyond visual design and included implementation of interactive logic, real-time behaviour, and feature integration.

---

## Tech Stack

- Python  
- Django  
- Django Channels (WebSockets)  
- JavaScript  
- HTML / CSS  
- Mapbox GL JS  
- Redis (used during development for real-time features)  

---

## Repository Structure

pulsepath/

├── manage.py

├── requirements.txt

├── map/ # map logic, views, templates, geofence handling

├── pulsepath/ # project config, routing, consumers, templates

├── static/ # icons and images used in the UI

├── docs/ # supporting project documents

└── res/ # reference assets

## Project Context

PulsePath began as a final-year university project and was later recognised through multiple awards.

The broader concept has since been explored further beyond the original prototype, including feasibility-stage work around its potential real-world application.

---

## Current Status

This repository represents a **prototype / portfolio project**.

It is not currently deployed as a production system, and configuration has been simplified for public sharing.

It should be viewed as:
- a demonstration of the problem and solution approach
- a showcase of the implementation and structure
- a reflection of my contribution to the project

---

## Notes

Some configuration (e.g. environment variables, API tokens) has been intentionally removed or replaced with placeholders for security.

---

## Acknowledgements

PulsePath was developed as a two-person final-year project.

This repository is shared as part of my personal portfolio to showcase my contribution.