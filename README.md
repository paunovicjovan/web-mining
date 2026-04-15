# Aspect-Based Sentiment Analysis of Product Reviews Using LangExtract

University seminar paper and implementation project - Web Mining course.

## Overview

This repository contains a seminar paper and a working implementation of an aspect-based sentiment analysis (ABSA) system for mobile phone reviews. Rather than assigning a single positive/negative label to an entire review, the system identifies specific product aspects (battery, camera, screen, etc.) and determines the sentiment expressed toward each one individually.

## Seminar Paper

The paper is written in Serbian and covers the theoretical background and practical implementation of the system. Topics covered:

- Web mining and opinion mining fundamentals
- Sentiment analysis — types, approaches, and the case for aspect-level analysis
- Information extraction and the LangExtract library
- Text embeddings - from Bag of Words to Sentence Transformers (SBERT)
- Text clustering - K-Means, DBSCAN, and Agglomerative Clustering in detail
- Full description of the implemented system, dataset, pipeline, and results

## Project

The implementation is a two-phase web application built with FastAPI and Streamlit. It uses the Amazon Unlocked Mobile Phones dataset (Kaggle) as its data source.

See [`Projekat/README.md`](./Projekat/README.md) for setup instructions, environment variables, and how to run the project.

## Tech Stack

`langextract` · `sentence-transformers` · `scikit-learn` · `FastAPI` · `Streamlit` · `SQLite`