
## Category A: State-of-the-Art & High-Complexity Models (Accuracy Benchmarks)

These models define the upper limit of accuracy. We study them to understand what makes them so effective, and potentially borrow concepts for more efficient models.

| Model | Architecture Breakdown | Strengths | Edge Feasibility Challenges |
|-----|----------------------|----------|-----------------------------|
| CRET / ECAPA-TDNN / Transformers | (As previously discussed) | Highest published accuracy on academic benchmarks. | Extremely high computational and memory requirements. Not a direct path to the edge without significant compromises. |
| Res2Net | Multi-Scale Residual Network: A variant of ResNet where a single residual block is replaced with a block that processes features at multiple scales. | Excellent at capturing features of varying importance within a single layer. Very strong accuracy. | Higher complexity and memory usage than a standard ResNet of equivalent depth. |
| D-TDNN | Deep Time Delay Neural Network: Stacks more TDNN layers to create a deeper network, often with residual connections. | Improved accuracy over the original x-vector TDNN by leveraging greater network depth. | Deeper networks lead to higher latency and memory usage. Risk of diminishing returns. |

## Category B: Efficient & Balanced 2D-CNNs (Primary Candidates)

These models treat an audio spectrogram as an image and are our strongest candidates due to the maturity of 2D-CNN optimization tools.

| Model | Architecture Breakdown | Strengths | Edge Feasibility Advantages |
|-----|----------------------|----------|-----------------------------|
| ResNet / MobileNet / GhostNet | (As previously discussed) | Excellent balance of accuracy and performance, with a wide range of available sizes and pre-trained weights. | Proven track record for edge deployment across many domains. The safest starting point. |
| EfficientNet | Compound Scaled CNN: A family of models where the depth, width, and input resolution are scaled up in a principled, balanced way. | Best-in-class accuracy-to-parameter ratio. A B0 or B1 version can outperform a larger ResNet with fewer resources. | Excellent candidate for quantization. The scaling principle allows you to pick a precise trade-off point. |
| ShuffleNet V2 | Channel Shuffle & Group Convolutions: An architecture designed to minimize memory access cost, a key bottleneck on edge hardware. | Specifically designed for low-power devices. Can be faster than MobileNetV2 at similar accuracy levels. | A very strong contender for CPU-bound inference tasks. |

## Category C: Efficient 1D Convolutional Models (Direct Audio Processing)

This is a powerful category that works on 1D audio representations (like raw waveforms or MFCCs). They are often more naturally suited to audio and can be very lightweight.

| Model | Architecture Breakdown | Strengths | Edge Feasibility Advantages |
|-----|----------------------|----------|-----------------------------|
| x-vector | TDNN + Statistics Pooling: The foundational architecture for modern speaker recognition. A stack of 1D convolutions (TDNN) captures temporal features, which are then aggregated across time into a single vector. | Simpler and lighter than its successor, ECAPA-TDNN. A very strong and well-understood baseline. | Excellent starting point. Likely to meet real-time goals on a Pi with good accuracy. Many open-source implementations. |
| RawNet2 | 1D-CNN on Raw Waveform: A deep stack of 1D convolutions, including residual connections and GRU layers, that learns directly from the raw audio signal. | No pre-processing needed (like MFCCs), simplifying the entire pipeline and saving CPU cycles. | Can be more robust as it lets the network learn the best possible filters, rather than being fixed to a pre-defined feature type. |
| SincNet | Parametric 1D-CNN: A novel 1D-CNN where the first layer's filters are not learned freely but are parameterized as sinc functions, forcing them to become meaningful band-pass filters. | Extremely efficient and fast. Converges much faster with less data. The first layer is interpretable and powerful. | A prime candidate for the edge. Its inherent efficiency makes it ideal for resource-constrained devices. |

## Category D: Hybrid Architectures (CNN + RNN)

These models combine the feature extraction power of CNNs with the sequence-handling capabilities of Recurrent Neural Networks (RNNs).

| Model | Architecture Breakdown | Strengths | Edge Feasibility Advantages |
|-----|----------------------|----------|-----------------------------|
| DeepSpeaker (VGG-Vox) | 2D-CNN + RNN/Aggregation: Uses a 2D-CNN (like VGG or ResNet) on spectrograms to extract frame-level features, which are then passed to an RNN (GRU/LSTM) or an aggregation layer to create the final utterance-level embedding. | Intuitive architecture that explicitly separates local feature extraction (CNN) and temporal aggregation (RNN). | RNNs can be slow to run on standard hardware due to their sequential nature. However, a lightweight CNN with a simple GRU layer can be a good balance. |

## Category E: Self-Supervised Learning (SSL) Models (Advanced/Future-Proof)

These are massive "foundation models" trained on enormous unlabeled audio datasets. They are generally too large to deploy directly, but they offer a powerful alternative approach.

| Model | Architecture Breakdown | Strengths | Edge Feasibility Strategy |
|-----|----------------------|----------|---------------------------|
| Wav2Vec 2.0 / HuBERT / WavLM | Transformer-based: Large Transformer networks trained to learn general-purpose representations of audio. | Incredibly powerful feature extractors. They learn the fundamental "language" of audio and are very robust to noise and domain shifts. | Not deployed directly. The strategy is "Feature Extraction + Lightweight Head." You use the massive SSL model (on a server, or a heavily optimized version on the edge) to convert audio into high-quality feature vectors, and then train a tiny, fast classification model (e.g., logistic regression or a small neural net) on those features. |

## Engineering Summary & Refined Decision Matrix

Let's consolidate this into a decision-making table to help select our final candidates.

| Category | Top Candidates | Input Type | Relative Complexity | Key Advantage for Edge Deployment |
|-------|---------------|-----------|--------------------|----------------------------------|
| Efficient 2D-CNNs | ResNet-34, EfficientNet-B0, GhostNet | Spectrogram | Medium | Highly optimizable, mature tools, great accuracy balance. |
| Efficient 1D-CNNs | x-vector, SincNet | MFCCs / Raw Waveform | Low-to-Medium | Designed for audio, very fast, simpler pipelines. |
| Hybrids | DeepSpeaker (with a light CNN) | Spectrogram | Medium | Good separation of concerns (feature vs. sequence). |
| SSL / Foundation | Wav2Vec 2.0 (Feature Extractor) | Raw Waveform | Very High (but separable) | State-of-the-art robustness if latency can be managed. |

Refined Action Plan
