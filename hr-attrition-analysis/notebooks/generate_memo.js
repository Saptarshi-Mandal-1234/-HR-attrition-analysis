const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
  BorderStyle, WidthType, ShadingType, PageNumber, TabStopType, TabStopPosition
} = require("docx");

const OUT = "/home/claude/hr_attrition_project/outputs";
const NAVY = "1F3864";
const RED = "C0392B";
const LIGHTBLUE = "DCE6F1";
const GREY = "595959";

const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const cellBorders = { top: border, bottom: border, left: border, right: border };

function headerCell(text, width) {
  return new TableCell({
    borders: cellBorders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: NAVY, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({
      children: [new TextRun({ text, bold: true, color: "FFFFFF", size: 20 })]
    })]
  });
}
function bodyCell(text, width, opts = {}) {
  return new TableCell({
    borders: cellBorders,
    width: { size: width, type: WidthType.DXA },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR } : undefined,
    children: [new Paragraph({
      children: [new TextRun({ text, size: 20, bold: opts.bold || false, color: opts.color || "000000" })]
    })]
  });
}

function img(name, w, h) {
  return new ImageRun({
    type: "png",
    data: fs.readFileSync(`${OUT}/${name}`),
    transformation: { width: w, height: h },
    altText: { title: name, description: name, name }
  });
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Calibri", color: NAVY },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 0,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 4 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Calibri", color: NAVY },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 1 } },
    ]
  },
  numbering: {
    config: [
      { reference: "recs", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.",
        alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•",
        alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } }
    },
    headers: {
      default: new Header({ children: [
        new Paragraph({
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
          children: [
            new TextRun({ text: "HR Attrition Analysis", bold: true, color: NAVY, size: 18 }),
            new TextRun({ text: "\tConfidential — Internal Use", color: GREY, size: 18 }),
          ]
        })
      ]})
    },
    footers: {
      default: new Footer({ children: [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", size: 18, color: GREY }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18, color: GREY }),
          ]
        })
      ]})
    },
    children: [
      // ---------- Title block ----------
      new Paragraph({
        children: [new TextRun({ text: "Employee Attrition Analysis", bold: true, size: 44, color: NAVY })],
        spacing: { after: 60 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "Insight Memo & Retention Recommendations", size: 26, color: GREY, italics: true })],
        spacing: { after: 200 }
      }),
      new Paragraph({
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        children: [
          new TextRun({ text: "Prepared by: Saptarshi Mandal", size: 20, color: GREY }),
          new TextRun({ text: "\tJune 2026", size: 20, color: GREY }),
        ],
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "BFBFBF", space: 4 } },
        spacing: { after: 280 }
      }),

      // ---------- Executive Summary ----------
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Executive Summary")] }),
      new Paragraph({
        spacing: { after: 160 },
        children: [new TextRun({
          text: "Of 1,470 employees analyzed, 237 (16.1%) left the company. Attrition is not random — it is concentrated among a clearly identifiable group: employees working overtime, in Sales and Laboratory Technician roles, who travel frequently, are single, sit in the lowest income quartile, and have gone the longest without a promotion. A logistic regression model trained on this pattern correctly flags 64% of actual leavers (vs. a 16% baseline), giving HR a usable early-warning tool rather than just a retrospective report.",
          size: 22
        })]
      }),

      // ---------- Key Findings ----------
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Key Findings")] }),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2400, 3960, 3000],
        rows: [
          new TableRow({ children: [headerCell("Driver", 2400), headerCell("Finding", 3960), headerCell("Risk Multiple", 3000)] }),
          new TableRow({ children: [bodyCell("Overtime", 2400), bodyCell("30.5% attrition with overtime vs. 10.4% without", 3960), bodyCell("~3.0x", 3000, { bold: true, color: RED })] }),
          new TableRow({ children: [bodyCell("Job Role", 2400, { fill: "F2F2F2" }), bodyCell("Sales Representatives: 39.8% attrition — the single highest-risk role", 3960, { fill: "F2F2F2" }), bodyCell("~8.1x vs. Research Director", 3000, { bold: true, color: RED, fill: "F2F2F2" })] }),
          new TableRow({ children: [bodyCell("Marital Status", 2400), bodyCell("Single employees: 25.5% vs. 12.5% for married employees", 3960), bodyCell("~2.0x", 3000)] }),
          new TableRow({ children: [bodyCell("Income", 2400, { fill: "F2F2F2" }), bodyCell("Lowest income quartile: 29.3% vs. 10.3% in the top quartile", 3960, { fill: "F2F2F2" }), bodyCell("~2.8x", 3000, { fill: "F2F2F2" })] }),
          new TableRow({ children: [bodyCell("Business Travel", 2400), bodyCell("Frequent travelers: 24.9% vs. 8.0% for non-travelers", 3960), bodyCell("~3.1x", 3000)] }),
          new TableRow({ children: [bodyCell("Tenure", 2400, { fill: "F2F2F2" }), bodyCell("Leavers average 5.1 years at the company vs. 7.4 years for stayers — exits cluster relatively early in tenure", 3960, { fill: "F2F2F2" }), bodyCell("—", 3000, { fill: "F2F2F2" })] }),
        ]
      }),
      new Paragraph({ text: "", spacing: { after: 200 } }),

      // ---------- Visual Highlights ----------
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Visual Highlights")] }),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [4680, 4680],
        rows: [
          new TableRow({ children: [
            new TableCell({ width: { size: 4680, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 80, right: 80 },
              children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [img("01_overall_attrition.png", 260, 260)] })] }),
            new TableCell({ width: { size: 4680, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 80, right: 80 },
              children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [img("02_attrition_by_overtime.png", 280, 210)] })] }),
          ]})
        ]
      }),
      new Paragraph({ text: "", spacing: { after: 160 } }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [img("03_attrition_by_jobrole.png", 480, 330)] }),
      new Paragraph({ text: "", spacing: { after: 100 } }),

      // ---------- Predictive Model ----------
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Predictive Model Summary")] }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({
          text: "A logistic regression model was trained on 44 encoded features (75/25 train-test split, stratified for class imbalance). On held-out test data, the model achieved 77.7% accuracy and a ROC-AUC of 0.81, correctly identifying 64% of employees who actually left. The chart below ranks the strongest statistical drivers of attrition risk, controlling for all other factors simultaneously.",
          size: 22
        })]
      }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [img("08_top_attrition_drivers.png", 480, 360)] }),
      new Paragraph({ text: "", spacing: { after: 100 } }),

      // ---------- Recommendations ----------
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Recommendations")] }),
      new Paragraph({ numbering: { reference: "recs", level: 0 }, spacing: { after: 100 }, children: [
        new TextRun({ text: "Cap or compensate overtime in Sales and Lab Technician roles: ", bold: true, size: 22 }),
        new TextRun({ text: "these two groups carry the highest combined overtime + role risk; consider overtime caps, shift redistribution, or an overtime premium tied to retention bonuses.", size: 22 })
      ]}),
      new Paragraph({ numbering: { reference: "recs", level: 0 }, spacing: { after: 100 }, children: [
        new TextRun({ text: "Review promotion velocity: ", bold: true, size: 22 }),
        new TextRun({ text: "\"Years Since Last Promotion\" is a top-15 statistical driver. Introduce structured 18–24 month promotion/career-conversation checkpoints, especially for tenure-track employees in years 3–6 (the window where most exits cluster).", size: 22 })
      ]}),
      new Paragraph({ numbering: { reference: "recs", level: 0 }, spacing: { after: 100 }, children: [
        new TextRun({ text: "Target retention budget using the risk score, not tenure alone: ", bold: true, size: 22 }),
        new TextRun({ text: "use the model's risk-scored employee list (471 employees flagged \"High Risk\") to prioritize stay interviews and retention offers rather than spreading HR effort evenly across the workforce.", size: 22 })
      ]}),
      new Paragraph({ numbering: { reference: "recs", level: 0 }, spacing: { after: 200 }, children: [
        new TextRun({ text: "Re-examine frequent-travel role design: ", bold: true, size: 22 }),
        new TextRun({ text: "frequent travelers churn at ~3x the rate of non-travelers; consider rotating travel-heavy assignments or adding travel-frequency caps for at-risk segments (single, early-tenure, lower-income).", size: 22 })
      ]}),

      // ---------- Methodology ----------
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Methodology & Data")] }),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 60 }, children: [
        new TextRun({ text: "Dataset: IBM HR Analytics Employee Attrition dataset, 1,470 employees, 35 original features, no missing values.", size: 22 })
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 60 }, children: [
        new TextRun({ text: "Tools: Python (pandas, scikit-learn, matplotlib/seaborn) for EDA and modeling; Power BI for the interactive dashboard.", size: 22 })
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 60 }, children: [
        new TextRun({ text: "Model: Logistic regression with standardized features and class-balanced weighting to correct for the 16% positive-class imbalance.", size: 22 })
      ]}),
      new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 200 }, children: [
        new TextRun({ text: "Validation: Stratified 75/25 train-test split; metrics reported on the held-out test set only (not training data).", size: 22 })
      ]}),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(`${OUT}/HR_Attrition_Insight_Memo.docx`, buffer);
  console.log("Memo created successfully.");
});
