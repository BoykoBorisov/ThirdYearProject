from tkinter import E

import torch
from audioset_dataset import AudiosetDataset
from torch.utils.data import DataLoader
from audioset_weight_generator import get_sampler
from model import EfficientAudioNet
from hear21passt.hear21passt.base import load_model
from panns_inference import AudioTagging, models
from train import train, weight_average_selected_states
if __name__== '__main__':
  # hyperparameters for training
  epoch_count = 10
  learning_rate = 0.0001
  learning_rate_decay = 0.5
  learning_rate_dacay_step = 2
  batch_size = 32
  warmup_iterations = 1000

  # hyperparameters for knowledge distilation
  teacher_inference_weight = 0.1
  teacher_inference_temperature = 2

  # hyperparameters for mixup
  mixup_rate = 0.9
  mixup_weight = 0.5

  # hyperparameters for weight averaging 
  should_apply_weight_averaging = True
  weight_averaging_start_epoch = 5
  weight_averaging_end_epoch = 9

  num_classes = 527
  efficientnet_size = 2

  dir_path_save_model_weights = r"/home/jupyter/ThirdYearProject/model_weights"
  dir_path_sample_weights = r"/home/jupyter/ThirdYearProject/datasets/weights/weights_unbalanced.csv"
  dir_path_samples_training = r"/home/jupyter/ThirdYearProject/data-loader2/output"
  dir_path_sample_validation = r"/home/jupyter/ThirdYearProject/data-loader2/output_eval"
  csv_path_training_samples = r"/home/jupyter/ThirdYearProject/datasets/Audioset/unbalanced_train_segments.csv"
  csv_path_validation_samples = r"/home/jupyter/ThirdYearProject/datasets/Audioset/eval_segments.csv"

  dataset_training = AudiosetDataset(data_path=dir_path_samples_training, csv_path=csv_path_training_samples,
                                     num_classes=num_classes, mixup_rate=mixup_rate, mixup_alpha=mixup_weight)

  dataset_validation = AudiosetDataset(data_path=dir_path_sample_validation, csv_path=csv_path_validation_samples,
                                       num_classes=num_classes, mixup_rate=0, mixup_alpha=0)

  weighted_sampler_training = get_sampler(dataset_training, dir_path_sample_weights)

  #sampler option acts like shuffle
  dataloader_training = DataLoader(dataset=dataset_training, batch_size=batch_size, 
                                   shuffle=False, 
                                   sampler=weighted_sampler_training,
                                   pin_memory=False, num_workers=4)

  dataloader_validation = DataLoader(dataset=dataset_validation, batch_size = 40, 
                                    shuffle=False, pin_memory=True, num_workers=4)

  model = EfficientAudioNet()
    
  weight_average_selected_states(model, ["best_map_model_params_90021158.pth","model_params_9_0.4117691391682516.pth","best_map_model_params_80028579.pth","best_map_model_params_80004579.pth"], dir_path_save_model_weights, dataloader_validation)
  
  #hear_passt_model
  # teacher_model = load_model()

  # for name, param in teacher_model.named_parameters():
    # param.requires_grad = False
  # teacher_model = None
  # teacher_model = models.Cnn14(sample_rate=16000, window_size=512, 
  #               hop_size=160, mel_bins=64, fmin=50, fmax=14000, 
  #               classes_num=527)
  # teacher_model.load_state_dict(torch.load(r"/home/jupyter/ThirdYearProject/Cnn14_16k_mAP=0.438.pth")["model"])
  # for name, param in teacher_model.named_parameters():
  #   param.requires_grad = False
  # teacher_model = AudioTagging(model=m)

#   train(model=model, teacher_model=teacher_model, dataloader_training=dataloader_training,
#         dataloader_validation=dataloader_validation, epoch_count=epoch_count, learning_rate=learning_rate,
#         learning_rate_decay=learning_rate_decay, learning_rate_dacay_step=learning_rate_dacay_step, warmup_iterations=warmup_iterations,
#         teacher_inference_weight=teacher_inference_weight, teacher_inference_temperature=teacher_inference_temperature,
#         should_apply_weight_averaging=should_apply_weight_averaging, weight_averaging_start_epoch=weight_averaging_start_epoch, 
#         weight_averaging_end_epoch=weight_averaging_end_epoch, dir_path_save_model_weights=dir_path_save_model_weights, stop_knowledge_distilation = None,
#         resume_training=True, resume_training_weights_path = "/home/jupyter/ThirdYearProject/model_weights/model_params_70000579_0.38516599193804224.pth", 
#         resume_epoch = 7)
  