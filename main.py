import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def parse_conversations(uploaded_files):
    silence_all = []
    overtalk_all = []
    call_summary = []

    for uploaded_file in uploaded_files:
        try:
            convo = json.load(uploaded_file)
            silences = []
            overtalks = []

            total_duration = convo[-1]["etime"] - convo[0]["stime"] if convo else 0

            for i in range(len(convo) - 1):
                curr = convo[i]
                next_ = convo[i + 1]

                gap = next_["stime"] - curr["etime"]
                if gap > 0:
                    silences.append(gap)
                    silence_all.append(gap)
                elif gap < 0:
                    overtalks.append(-gap)
                    overtalk_all.append(-gap)

            silence_time = sum(silences)
            overtalk_time = sum(overtalks)

            call_summary.append({
                "File Name": uploaded_file.name,
                "Total Duration (s)": round(total_duration, 2),
                "Total Silence (s)": round(silence_time, 2),
                "Total Overtalk (s)": round(overtalk_time, 2),
                "Silence %": round((silence_time / total_duration) * 100, 2) if total_duration else 0,
                "Overtalk %": round((overtalk_time / total_duration) * 100, 2) if total_duration else 0,
                "Avg. Silence (s)": round(sum(silences) / len(silences), 2) if silences else 0,
                "Avg. Overtalk (s)": round(sum(overtalks) / len(overtalks), 2) if overtalks else 0,
            })

        except Exception as e:
            st.error(f"Error in file {uploaded_file.name}: {e}")

    return silence_all, overtalk_all, call_summary

def plot_histogram(data, title, xlabel, color):
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Set overall theme
    sns.set_theme(style="darkgrid")
    plt.style.use("dark_background")

    # Create pastel color map
    pastel_color = sns.color_palette("pastel")[0] if not color else color

    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot histogram with pastel fill and black edges
    n, bins, patches = ax.hist(
        data,
        bins=20,
        color=pastel_color,
        edgecolor='white',
        alpha=0.85,
        density=True
    )
    

    # Bar styling: apply pastel color and hover effect
    for patch in patches:
        patch.set_linewidth(1.2)
        patch.set_linestyle('-')

    # Layout and grid settings
    ax.set_xlim(0, max(data) * 1.1)
    ax.set_ylim(0, 1)
    ax.set_facecolor("#1e1e1e")  # dark charcoal background for axes
    fig.patch.set_facecolor("#2c2f33")  # slightly lighter background for figure

    ax.set_title(title, fontsize=16, color='white', pad=15)
    ax.set_xlabel(xlabel, fontsize=12, color='lightgray')
    ax.set_ylabel("Frequency", fontsize=12, color='lightgray')

    # Customize ticks
    ax.tick_params(colors='gray', which='both')

    st.pyplot(fig)


def main():
    st.set_page_config("📞 Silence & Overtalk Metrics", layout="wide")
    st.title("📊 Silence and Overtalk Metrics Dashboard")

    uploaded_files = st.file_uploader("Upload one or more conversation JSON files", type="json", accept_multiple_files=True)

    if uploaded_files:
        st.divider()
        st.subheader("📁 Processing Conversations...")
        silence_durations, overtalk_durations, summary = parse_conversations(uploaded_files)

        st.success(f"Analyzed {len(uploaded_files)} conversations.")

        col1, col2 = st.columns(2)

        with col1:
            if silence_durations:
                st.markdown("### 🔇 Silence Duration Histogram")
                plot_histogram(silence_durations, "Silence Duration Distribution", "Duration (seconds)", "dodgerblue")
            else:
                st.warning("No silence detected.")

        with col2:
            if overtalk_durations:
                st.markdown("### 🗣️ Overtalk Duration Histogram")
                plot_histogram(overtalk_durations, "Overtalk Duration Distribution", "Duration (seconds)", "tomato")
            else:
                st.warning("No overtalk detected.")

        st.divider()

        st.markdown("### 📋 Summary Metrics per Call")
        df_summary = pd.DataFrame(summary)
        st.dataframe(df_summary, use_container_width=True)

        # Show overall metrics at a glance
        if df_summary.shape[0] > 0:
            st.markdown("### 📈 Overall Averages Across All Calls")
            avg_row = {
                "Avg Silence %": round(df_summary["Silence %"].mean(), 2),
                "Avg Overtalk %": round(df_summary["Overtalk %"].mean(), 2),
                "Avg Silence Duration": round(df_summary["Avg. Silence (s)"].mean(), 2),
                "Avg Overtalk Duration": round(df_summary["Avg. Overtalk (s)"].mean(), 2),
            }

            st.metric("📊 Avg. Silence %", f"{avg_row['Avg Silence %']}%")
            st.metric("🗣️ Avg. Overtalk %", f"{avg_row['Avg Overtalk %']}%")
            st.metric("⏱️ Avg. Silence Duration", f"{avg_row['Avg Silence Duration']} s")
            st.metric("🔁 Avg. Overtalk Duration", f"{avg_row['Avg Overtalk Duration']} s")

if __name__ == "__main__":
    main()
