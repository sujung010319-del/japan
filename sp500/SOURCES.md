# 출처 표기

## 2006–2010년 편입·편출 건수

**이 구간은 단일 출처다.** tickericons.com은 이 구간이 성겨서 쓸 수 없고
(2006년 1건만 수록, 실제로는 32건), S&P 공식 집계 문서는 접근하지 못했다.
아래를 그대로 인용하면 된다.

### 인용문 (국문)

> S&P 500 구성종목 이력 데이터셋(fja05680/sp500, `S&P 500 Historical Components &
> Changes (Updated).csv`)의 날짜별 구성종목을 인접 시점끼리 대조해 산출. 2026년 8월 24일
> 내려받음. 해당 데이터셋의 원출처는 Andreas Clenow, *Trading Evolved*(2019) 부속
> 데이터(1996–2019) 및 위키피디아 "List of S&P 500 companies" 변경 이력이다.

### 인용문 (영문)

> Computed by diffing consecutive daily constituent lists in the S&P 500 historical
> components dataset (fja05680/sp500, `S&P 500 Historical Components & Changes
> (Updated).csv`), retrieved 24 Aug 2026. That dataset derives from the companion data
> to Andreas Clenow, *Trading Evolved* (2019) for 1996–2019, updated thereafter from
> Wikipedia's "List of S&P 500 companies" change log.

### 데이터 지문 (재현·검증용)

| 항목 | 값 |
|---|---|
| URL | https://raw.githubusercontent.com/fja05680/sp500/master/S%26P%20500%20Historical%20Components%20%26%20Changes%20(Updated).csv |
| 저장소 | https://github.com/fja05680/sp500 |
| 내려받은 날 | 2026-08-24 |
| SHA-256 | `39a9202c9ef69a74c0ff07e2113ad41fb6da7c8c5b6cd9541f0185fb4391e717` |
| 크기 | 5,526,653 bytes |
| 행 수 | 2,718 (헤더 제외) |
| 수록 기간 | 1996-01-02 ~ 2026-06-30 |
| 2006년 행 수 | 114 |

### 반드시 함께 적을 한계

1. **1차 출처가 아니다.** 위키피디아 파생 커뮤니티 데이터셋이며 S&P Dow Jones Indices의
   공식 집계가 아니다.
2. **티커 변경이 중복 집계된다.** 사명·티커 변경이 편입 1건 + 편출 1건으로 잡힌다.
   최근 연도 기준 연 2~4건.
3. **2006–2010년 합계는 교차 검증되지 않았다.** 개별 사건 3건만 1차 출처로 확인했다
   (아래). 연간 총계 자체를 독립적으로 확인한 출처는 없다.

### 2006년 개별 사건 1차 출처 확인분

| 사건 | 1차 출처 |
|---|---|
| Google, 2006-03-31 편입 (Burlington Resources 대체) | https://www.nbcnews.com/id/wbna11981777 · https://www.cbsnews.com/news/google-to-join-the-sp-500/ |
| CME, 2006-08-10 종가 기준 편입 | https://www.cmegroup.com/media-room/press-releases/2006/8/04/chicago_mercantileexchangeholdingsincnamedtosp500index.html |
| HCA, 2006-11-17 LBO 완료로 상장폐지·편출 | https://investor.hcahealthcare.com/news/news-details/2006/HCA-Completes-Merger-With-Private-Investor-Group/default.aspx |

---

## 더 강한 출처로 바꾸고 싶다면 (권장 순)

논문·보고서 등 검증이 필요한 문서라면 아래로 교체하는 편이 낫다.

**1. S&P Dow Jones Indices 공식 리서치 — 최상위**
"What Happened to the Index Effect? A Look at Three Decades of S&P 500 Adds and Drops"
1995년 1월 ~ 2021년 6월 편입·편출 전수를 S&P가 직접 집계.
- https://www.spglobal.com/spdji/en/research/article/what-happened-to-the-index-effect-a-look-at-three-decades-of-sp-500-adds-and-drops/
- PDF: https://www.spglobal.com/spdji/en/documents/research/research-what-happened-to-the-index-effect.pdf
- 2006~2021 구간을 이걸로 덮으면 위 한계 3가지가 전부 해소된다.

**2. Greenwood & Sammon, "The Disappearing Index Effect" (NBER WP 30748) — 학술 인용 가능, 무료**
연도별 편입·편출 건수 표 수록. 1980년대~2020년대 커버.
- https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
- HBS 버전: https://www.hbs.edu/ris/Publication%20Files/23-025_563e45c6-df92-4d9c-ae05-608d4d0acab1.pdf

**3. CRSP / Compustat (WRDS 경유) — 금융 실증연구 표준**
S&P 500 구성종목 변경의 사실상 표준 데이터. 기관 구독 필요.
- https://wrds-www.wharton.upenn.edu/classroom/sp500-introduction/over-time/

**4. S&P DJI 개별 보도자료 — 건별 1차 출처**
2012년 이후만 아카이브에 남아 있어 2006~2010년에는 쓸 수 없다.
이 저장소의 `press_releases_2012_2026.csv`에 160건 수록.
- https://press.spglobal.com/index.php?s=2429

**5. tickericons.com — 2011년 이후만**
2011~2018년은 위 데이터셋과 오차 0~2로 일치하나 2006~2010년은 결측이 심하다.
- https://tickericons.com/changes
