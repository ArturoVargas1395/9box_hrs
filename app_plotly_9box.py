import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==============================
# 🎨 CONFIGURATION
# ==============================
COLOR_LIGHT = "#d9d9d9"
COLOR_MEDIUM = "#bfbfbf"
COLOR_DARK = "#808080"
COLOR_POINTS = "#800080"  # Purple

# Quadrant titles and descriptions
quadrants = {
    (0, 0): ("1️ Question & Develop", "Low HTO & Performance."),
    (1, 0): ("2️ Solid Contributor", "Average HTO, low performance."),
    (2, 0): ("3️ Good Performer", "High HTO, low performance."),
    (0, 1): ("4️ Out of Focus", "Low HTO, average performance."),
    (1, 1): ("5️ Core Player", "Average HTO & performance."),
    (2, 1): ("6️ High Impact", "High HTO, good performance."),
    (0, 2): ("7️ Enigma", "Low HTO, high performance."),
    (1, 2): ("8️ High Potential", "Average HTO, high performance."),
    (2, 2): ("9️ Star", "High HTO & high performance.")
}

colors = {
    (0, 0): COLOR_LIGHT,
    (1, 0): COLOR_LIGHT,
    (0, 1): COLOR_LIGHT,
    (2, 0): COLOR_MEDIUM,
    (1, 1): COLOR_MEDIUM,
    (0, 2): COLOR_MEDIUM,
    (2, 1): COLOR_DARK,
    (1, 2): COLOR_DARK,
    (2, 2): COLOR_DARK,
}

# ==============================
# 🚀 STREAMLIT APP
# ==============================
st.set_page_config(page_title="📊 9-Box Talent Matrix (Plotly)", layout="wide")
st.title("📊 9-Box Talent Matrix Dashboard")

uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Load data
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
        required_cols = ["Name", "HTO", "Performance"]

        if not all(col in df.columns for col in required_cols):
            st.error("❌ File must contain columns: Name, HTO, Performance")
        else:
            df["HTO"] = df["HTO"].round(2)
            df["Performance"] = df["Performance"].round(2)

            fig = go.Figure()

            # Draw quadrants as background rectangles
            for (i, j), color in colors.items():
                fig.add_shape(
                    type="rect",
                    x0=i*2, x1=(i+1)*2,
                    y0=j*2, y1=(j+1)*2,
                    fillcolor=color,
                    opacity=0.4,
                    line_width=0
                )
                # Add quadrant titles
                title, _ = quadrants[(i, j)]
                fig.add_annotation(
                    x=i*2+0.5, y=j*2+1.5,
                    text=title,
                    showarrow=False,
                    font=dict(size=10, color="black")
                )

            # Add scatter points (names only visible on hover)
                fig.add_trace(go.Scatter(
                x=df["HTO"],
                y=df["Performance"],
                mode="markers",  # ✅ No permanent text outside dots
                text=df["Name"],  # used for hover
                marker=dict(
                size=12,
                color=COLOR_POINTS,
                line=dict(width=1, color='black')
                ),
                hovertemplate="<b>👤 %{text}</b><br>🔥 HTO: %{x}<br>📈 Performance: %{y}<extra></extra>",
                showlegend=False  # ✅ This removes the trace_0, trace_1 legends
                ))


            # Update layout
            fig.update_layout(
                title="9-Box Talent Matrix",
                xaxis=dict(title="HTO Score", range=[0, 6], dtick=1, gridcolor='lightgrey'),
                yaxis=dict(title="Performance Score", range=[0, 6], dtick=1, gridcolor='lightgrey'),
                plot_bgcolor="white",
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

            # Legend
            st.subheader("📖 Quadrant Legend")
            for key, (title, desc) in quadrants.items():
                st.markdown(f"**{title}** – {desc}")

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
else:
    st.info("⬆️ Upload an Excel file to visualize your matrix.")
