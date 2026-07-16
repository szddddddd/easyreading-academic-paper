# 领域解释检查表

只读取并应用与当前论文相关的部分。跨领域论文合并使用，避免同一符号在不同领域语义下混淆。

## 1. 计算机视觉

解释视觉模型时检查：

- 输入图像、视频、feature map、token 或 patch 的形状与布局；
- 图像坐标的原点、轴方向、像素中心约定和归一化范围；
- resize、crop、padding、augmentation 与相机标定是否改变几何关系；
- CNN 的 stride、receptive field、channel；Transformer 的 patch size、token 数、attention 范围和位置编码；
- 局部特征与全局特征如何交互；
- detection、segmentation、flow、depth、pose 等输出的坐标与尺度；
- supervision 来自哪里，loss 对哪些层和变量回传；
- train/test 分辨率、multi-scale、sliding window 和后处理差异；
- 指标的具体定义，例如 IoU、AP、PSNR、SSIM、LPIPS、EPE，以及数值方向。

## 2. 多视图几何与三维重建

至少说明：

- 世界坐标、相机坐标、归一化成像平面、像素坐标之间的变换；
- 内参 K、外参 R/t、齐次坐标、投影和反投影；
- 深度、逆深度、视差、尺度和 gauge ambiguity；
- correspondence、epipolar constraint、triangulation、PnP、bundle adjustment 的输入输出；
- visibility、occlusion、view overlap 和置信度；
- photometric、reprojection、geometric consistency、normal 或 regularization loss；
- 标定误差、动态物体、非朗伯表面、弱纹理和曝光变化带来的失败条件；
- mesh、point cloud、voxel、implicit field、radiance field 等表示的差异与转换。

公式涉及投影时，明确列出：

    world point -> camera transform -> perspective division -> pixel transform

若论文采用 row-vector、column-vector 或不同轴约定，严格沿用原文。

## 3. 前馈式三维重建

对 feed-forward 3D reconstruction 论文，首先区分“一次或少数几次网络前向计算得到场景表示”与“针对每个场景持续优化参数”。若方法包含 test-time refinement，明确拆分前馈预测和后续优化各自的输入、耗时与贡献。

至少说明：

- 输入是单图、图像对、无序多视图、顺序视频还是混合模态，视图数量与分辨率是否可变；
- 相机内外参是已知、部分已知、联合预测还是完全未知；
- 图像 encoder、跨视图 attention、matching/correlation、global token 与 prediction head 的张量形状和信息流；
- 方法显式建立 correspondence，还是在网络特征中隐式完成跨视图关联；
- 输出是 depth、point map、camera pose、point cloud、mesh、voxel、implicit field、radiance field、triplane 还是 Gaussian；
- 输出位于各相机坐标、参考视图坐标、规范坐标还是统一世界坐标；
- 全局尺度、旋转、平移及反射歧义如何固定，评测前是否执行 Sim(3)、SE(3) 或尺度对齐；
- 多视图顺序是否影响结果，模型是否具有 permutation invariance/equivariance；
- 可变视图数量如何训练，长序列是否使用分块、层次聚合、memory 或 recurrent update；
- confidence、visibility、occlusion 与无重叠视图如何建模；
- camera、geometry 与 appearance 是联合预测、交替预测还是分阶段恢复；
- supervision 来自真实几何、SfM/MVS 伪标签、渲染、合成数据还是自监督一致性；
- point/depth、pose、reprojection、matching、rendering、confidence 和 regularization loss 分别约束什么；
- 训练数据中的场景、相机、焦距、基线和视图数量分布，与测试分布有何差异；
- 一次前向耗时是否包含特征提取、相机恢复、几何融合、表示转换和可选 refinement；
- cross-view attention、cost volume 或 all-pairs matching 随视图数与像素/token 数的时间和显存复杂度；
- 单场景精度、跨数据集泛化、零样本能力和大规模场景扩展分别如何评测；
- pose、depth、point cloud、surface、novel-view synthesis 等指标是否在相同对齐方式和可见区域上计算；
- 重复纹理、低纹理、极窄/极宽基线、未知焦距、动态物体和跨域图像如何导致失败；
- 前馈结果与传统 SfM/MVS、优化式 NeRF/3DGS 以及其他 generalizable reconstruction 方法是否在相同输入和预算下比较。

若网络直接预测 3D Gaussian、radiance field 或其他可渲染表示，继续应用 Gaussian Splatting 或可微渲染检查表，解释预测表示如何进入 renderer，以及渲染损失是否反向约束相机与几何。

## 4. 计算机图形学与可微渲染

解释渲染方程或 rasterization/ray tracing 时检查：

- scene representation、camera、light、material 和背景；
- ray origin/direction、near/far、采样位置和步长；
- geometry、BRDF/BSDF、radiance、density、transmittance 与 visibility；
- forward rendering 的积分、离散近似、排序和合成顺序；
- screen-space footprint、anti-aliasing、clipping 和 depth test；
- 哪些操作可微，梯度对几何、材质、光照和相机如何传播；
- visibility discontinuity、Monte Carlo variance、近似 bias 和数值稳定性；
- 时间、显存、分辨率和场景规模复杂度。

不要把 physically based rendering、volume rendering 和 alpha compositing 混为同一个过程。

## 5. Gaussian Splatting

对 3D/4D Gaussian Splatting 至少解释：

- 每个 Gaussian 的中心、尺度、旋转、协方差、opacity、颜色或 spherical harmonics 参数；
- 协方差如何由尺度与旋转构造，参数化如何保证半正定；
- 世界空间 Gaussian 如何经相机变换与投影 Jacobian 得到屏幕空间 footprint；
- depth 或 tile 排序、可见性筛选、opacity 计算、transmittance 与 front-to-back alpha compositing；
- 颜色、几何、opacity、相机和外观参数中哪些可学习、梯度如何回传；
- initialization、densification、split/clone、pruning、opacity reset 的触发条件；
- 静态、动态、可变形、时序或语义 Gaussian 的额外状态；
- rasterizer 的近似、排序误差、过度重叠、floaters、holes 和显存增长；
- 训练与渲染速度的测量条件，避免把不同分辨率或硬件的 FPS 直接比较。

若论文修改 3DGS 的某个组件，先完整说明标准 3DGS 对应流程，再指出修改发生在参数化、投影、排序、合成、优化还是 densification。

## 6. 生成式深度学习

区分并定义：

- 数据变量 x、条件 c、latent z、noise epsilon、时间步 t 和模型预测量；
- encoder/decoder、prior/posterior、score、velocity、noise 或 clean-data parameterization；
- forward/noising process 与 reverse/denoising or sampling process；
- 训练时抽样了什么，目标函数预测什么；推理时从什么分布开始，经过哪些更新；
- noise schedule、SNR、guidance、temperature、solver 和采样步数；
- likelihood、ELBO、reconstruction、adversarial、perceptual 或 distillation loss 的角色；
- classifier-free guidance 的 conditional/unconditional 分支与尺度；
- autoregressive factorization 中 token 顺序、context、teacher forcing 和 exposure bias；
- 生成质量、diversity、alignment、likelihood 与效率指标之间的差异。

不要把训练目标、模型输出参数化和采样器视为同一个概念。

## 7. 世界模型

明确说明：

- observation o、latent/state s 或 z、action a、reward r、termination 和 context；
- state 是否显式包含深度、点、相机、occupancy、Gaussian 或其他三维结构，以及它使用哪个坐标系；
- representation model、transition/dynamics model、observation/reward decoder、policy/value model；
- deterministic 与 stochastic state 如何组合；
- posterior inference 与 prior prediction 在训练和 rollout 中分别何时使用；
- action-conditioned transition、rollout horizon 和 open-loop/closed-loop；
- reconstruction、prediction、KL、reward、value、consistency 或 contrastive objective；
- compounding error、posterior collapse、state aliasing 和 distribution shift；
- 相机或智能体运动如何进入 action，跨时间步的三维状态如何配准、更新与保持对象永久性；
- planning、MPC、imagination rollout 或 policy learning 如何消费预测状态；
- 环境交互数据、离线数据和生成数据之间的边界；
- 评估是在像素预测、latent prediction、控制回报还是下游任务上进行。
- 若声称具有三维一致性，评估是否真正测量 geometry、pose、cross-view consistency 和长期重访，而不只测视频感知质量。

说明“世界模型预测得像”“世界模型保持三维一致”“世界模型支持有效决策”是三个不同命题，分别检查证据。

## 8. 跨领域论文

常见组合及重点：

| 组合 | 必须连接的链条 |
|---|---|
| 生成模型 + 3D 重建 | 2D/latent 先验如何约束几何，梯度或采样结果如何回到 3D 表示 |
| 前馈三维重建 + 3DGS | 网络如何从图像直接预测 Gaussian 参数，是否仍需场景级 refinement，渲染监督如何回到相机与几何 |
| 前馈三维重建 + 世界模型 | observation 序列如何前馈恢复相机与几何，如何形成持久三维 state，再由 action-conditioned transition 进行更新和 rollout |
| 3DGS + 动态场景 | 时间/形变状态如何改变 Gaussian，时序一致性和可见性如何处理 |
| 世界模型 + 视频生成 | observation/state/action 与视频 latent/noise 的映射，控制信号如何进入生成过程 |
| 神经渲染 + 几何 | 几何、外观、光照和相机的可辨识性，以及 photometric loss 的退化解 |
| 多模态模型 + 视觉/3D | tokenization、cross-attention、坐标/位置编码与监督信号如何对齐 |

对于跨领域方法，画出一个统一信息流，并在每条边标明张量、坐标系或随机变量语义。不要分别讲完两个领域后遗漏它们真正交互的位置。

对于“前馈三维重建世界模型”，至少画清：

    context observations
      -> feed-forward camera/geometry inference
      -> persistent 3D state
      -> action-conditioned state transition
      -> future geometry/observation prediction
      -> planning or evaluation

逐步检查初始重建误差、坐标 gauge、遮挡区域补全、动态对象更新和 rollout 累积误差如何沿这条链传播。
